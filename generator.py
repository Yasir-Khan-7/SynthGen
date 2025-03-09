import streamlit as st
import pandas as pd
import re
from sdv.metadata import SingleTableMetadata
from sdv.single_table import GaussianCopulaSynthesizer

st.set_page_config(page_title="SynthGen", page_icon="🚀")

# Custom Styles
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton > button { background-color: #4CAF50; color: white; border-radius: 10px; }
    .stFileUploader > div { border: 2px dashed #4A90E2; }
    .stDataFrame { border-radius: 10px; overflow: hidden; }
    h1 { text-align: center; color: #4A90E2; }
    </style>
""", unsafe_allow_html=True)

# Function to extract year and increment properly
def increment_years(start_year, num_rows):
    """Generate a list of years continuing the existing format YYYY-YY."""
    years = []
    for i in range(num_rows):
        next_year = start_year + i
        short_next_year = str(next_year + 1)[-2:]  # Last two digits of next year
        years.append(f"{next_year}-{short_next_year}")
    return years

# Function to generate synthetic data dynamically
def generate_sdv_data(df, num_rows, pk_column=None):
    metadata = SingleTableMetadata()
    metadata.detect_from_dataframe(df)

    # Handle primary key if specified
    if pk_column:
        metadata.primary_key = None  # Remove PK designation for training
        metadata.update_column(pk_column, sdtype="categorical")  # Treat as categorical

    # Train synthesizer
    synthesizer = GaussianCopulaSynthesizer(metadata)
    synthesizer.fit(df)

    # Generate synthetic data
    synthetic_data = synthesizer.sample(num_rows)

    # Ensure column order matches original dataset
    synthetic_data = synthetic_data[df.columns]

    # Fix Year Column (if exists)
    if "Year" in df.columns:
        last_year_match = re.search(r"(\d{4})", str(df["Year"].max()))
        if last_year_match:
            last_year = int(last_year_match.group(1))
            synthetic_data["Year"] = increment_years(last_year, num_rows)
        else:
            st.warning("⚠️ Could not recognize year format, keeping generated values as is.")

    return synthetic_data

# Streamlit UI
st.sidebar.title("🌟 Synthetic Data Generator")

# Upload dataset
uploaded_file = st.sidebar.file_uploader("📂 Upload a dataset (CSV)", type=["csv"], help="Supported format: CSV")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📊 Uploaded Data Preview")
    st.dataframe(df.head(), use_container_width=True)

    # Let user select primary key column
    pk_column = st.selectbox("🔑 Select Primary Key Column (if any)", ["None"] + list(df.columns))
    pk_column = None if pk_column == "None" else pk_column

    # Number of rows input
    num_rows = st.number_input("🔢 Number of rows", min_value=1, value=len(df))

    if st.button("🚀 Generate Synthetic Data", use_container_width=True):
        st.write("🔄 Generating synthetic data...")

        try:
            df_sdv = generate_sdv_data(df, num_rows, pk_column)

            st.success("✅ Synthetic data generated successfully!")

            st.subheader("📊 Synthetic Data Preview")
            st.dataframe(df_sdv, use_container_width=True)

            st.download_button("⬇️ Download CSV", df_sdv.to_csv(index=False), "synthetic_data.csv", help="Download the generated data.")
        except Exception as e:
            st.error(f"⚠️ Error generating synthetic data: {str(e)}")

st.markdown("""<hr style='border: 1px solid #4A90E2;'>""", unsafe_allow_html=True)

st.info("✨ This tool uses the SDV library to generate realistic synthetic data based on your input dataset.")
