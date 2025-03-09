import streamlit as st
import pandas as pd
import asyncio
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from io import StringIO

st.set_page_config(page_title="SynthGen", page_icon="🚀")

# Initialize AI agent
model = GroqModel('llama-3.3-70b-versatile', api_key='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')  # Replace with actual API key
agent = Agent(model)

async def generate_synthetic_data(df: pd.DataFrame, num_rows: int) -> pd.DataFrame:
    column_info = "\n".join([f"{col}: {df[col].dtype} (example: {df[col].dropna().sample(1).values[0]})" for col in df.columns])
    prompt = (
        f"Generate {num_rows} rows of synthetic data similar to this dataset. "
        f"Ensure the same columns, data types, and realistic values.\n\n"
        f"Column details:\n{column_info}\n\n"
        f"Output only valid CSV data with correct delimiters and no additional text."
    )
    
    response = await agent.run(prompt)
    
    try:
        csv_data = response.data.strip()
        df_synthetic = pd.read_csv(StringIO(csv_data))
        
        # Ensure data types match original dataset
        for col in df.columns:
            if col in df_synthetic.columns:
                df_synthetic[col] = df_synthetic[col].astype(df[col].dtype, errors='ignore')
        
    except Exception as e:
        st.error(f"Error parsing generated data: {e}")
        return pd.DataFrame()
    
    return df_synthetic

st.sidebar.title("🌟 Synthetic Data Generator")

uploaded_file = st.sidebar.file_uploader("📂 Upload a CSV dataset", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df.head())
    num_rows = st.number_input("🔢 Number of rows", min_value=1, value=len(df))

    if st.button("🚀 Generate Synthetic Data"):
        async def async_generate():
            df_synthetic = await generate_synthetic_data(df, num_rows)
            if not df_synthetic.empty:
                st.dataframe(df_synthetic)
                st.download_button("⬇️ Download CSV", df_synthetic.to_csv(index=False), "synthetic_data.csv")
        asyncio.run(async_generate())
