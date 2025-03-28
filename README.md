# SynthGen AI

SynthGen AI is a Streamlit application that uses advanced Large Language Models (LLMs) to generate high-quality synthetic data based on your original dataset. The synthetic data maintains the statistical properties of your original data while ensuring privacy and confidentiality.

## Features

- **Privacy Preserving**: Generate synthetic data without exposing sensitive information
- **AI-Powered**: Leverages state-of-the-art LLMs to understand and replicate data patterns
- **Statistically Valid**: Maintains distributions and relationships present in your original data
- **User-Friendly Interface**: Simple upload, configure, and generate workflow
- **Data Visualization**: Compare original and synthetic data distributions

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/SynthGen.git
cd SynthGen

# Install required packages
pip install -r requirements.txt
```

## Usage

```bash
# Run the Streamlit app
streamlit run generator.py
```

## Environment Variables

This application requires a Groq API key. You can set it directly in the code or use an environment variable:

```bash
export GROQ_API_KEY=your_api_key_here
```

## How to Use

1. **Upload Data**: Start by uploading your CSV file using the uploader in the sidebar.
2. **Configure Options**: Set the number of rows you wish to generate.
3. **Generate Data**: Click the "Generate Data" button to start the generation process.
4. **Explore Results**: View and download your synthetic data from the Results tab.
5. **Visualize**: Compare the original and synthetic data distributions in the Visualization tab.

## Deployment

### Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Add your Groq API key as a secret
5. Deploy the app

## License

MIT

## Acknowledgements

- Built with [Streamlit](https://streamlit.io/)
- Uses [Groq](https://groq.com/) for LLM inference
- Visualization with [Plotly](https://plotly.com/)
