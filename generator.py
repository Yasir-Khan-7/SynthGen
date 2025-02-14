import streamlit as st
import pandas as pd
from sdv.metadata import SingleTableMetadata
from sdv.single_table import GaussianCopulaSynthesizer

# Function to dynamically detect metadata and generate synthetic data
def generate_sdv_data(uploaded_file, num_rows):
    df = pd.read_csv(uploaded_file)

    # Automatically detect metadata
    metadata = SingleTableMetadata()
    metadata.detect_from_dataframe(df)

    # Remove primary key constraint to treat it as a normal column
    if metadata.primary_key:
        pk_column = metadata.primary_key
        metadata.primary_key = None  # Remove PK designation
        metadata.update_column(pk_column, sdtype="categorical")  # Treat as categorical

    # Train GaussianCopulaSynthesizer with detected metadata
    synthesizer = GaussianCopulaSynthesizer(metadata)
    synthesizer.fit(df)

    # Generate synthetic data
    synthetic_data = synthesizer.sample(num_rows)

    # Ensure column order matches original dataset
    synthetic_data = synthetic_data[df.columns]

    return synthetic_data

# Streamlit UI
st.title("Synthetic Data Generator 🚀")

# Upload dataset
uploaded_file = st.file_uploader("📂 Upload a dataset (CSV)", type=["csv"])

num_rows = st.number_input("🔢 Number of rows", min_value=1, value=100)

if uploaded_file:
    st.write("🔄 Generating synthetic data...")
    
    try:
        df_sdv = generate_sdv_data(uploaded_file, num_rows)
        st.dataframe(df_sdv)
        st.download_button("⬇️ Download CSV", df_sdv.to_csv(index=False), "synthetic_data.csv")
    except Exception as e:
        st.error(f"⚠️ Error generating synthetic data: {str(e)}")
