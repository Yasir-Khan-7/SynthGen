import streamlit as st
import pandas as pd
import asyncio
import time
import plotly.express as px
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.providers.groq import GroqProvider
from io import StringIO, BytesIO
import os

# Set page configuration
st.set_page_config(
    page_title="SynthGen AI",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a modern look
st.markdown("""
<style>
    /* Modern Color Palette */

            header {
        border-bottom: 3px solid #136a8a !important;
    }
    [data-testid="stSidebar"] {
           background: linear-gradient(135deg, #73C8A9, #0b8793) !important;
        margin-top: 58px;
        box-shadow: 3px 0px 10px rgba(0, 0, 0, 0.15) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    :root {
        --primary: #00bf8f;
        --primary-light: #33cf9e;
        --primary-dark: #00a67a;
        --secondary: #6c757d;
        --success: #28a745;
        --info: #17a2b8;
        --warning: #ffc107;
        --danger: #dc3545;
        --orange: #fd7e14;
        --purple: #6f42c1;
        --teal: #20c997;
        --indigo: #6610f2;
        --light: #f8f9fa;
        --dark: #343a40;
        --white: #ffffff;
        --gray-100: #f8f9fa;
        --gray-200: #e9ecef;
        --gray-300: #dee2e6;
        --gray-400: #ced4da;
        --gray-500: #adb5bd;
        --gray-600: #6c757d;
        --gray-700: #495057;
        --gray-800: #343a40;
        --gray-900: #212529;
    }

    /* Global Styles */
    .stApp {
        background: var(--white);
    }

    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        font-weight: 600;
    }
    
    p, span, label, div {
        color: #000000 !important;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 1.05rem;
        line-height: 1.6;
    }

    /* Main Header */
    .main-header {
        color: #000000 !important;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin: 2rem 0;
        background: none;
        -webkit-background-clip: unset;
        -webkit-text-fill-color: unset;
        animation: none;
    }

    .sub-header {
        color: #000000 !important;
        font-size: 1.4rem;
        font-weight: 500;
        text-align: center;
        margin-bottom: 2rem;
    }

    /* Sidebar */
   
    
    /* File uploader styling */
    [data-testid="stFileUploaderDropzone"] {
        background: rgba(0, 191, 143, 0.2) !important; /* Light green background */
        display: flex;
        max-width: 100%;
        width: 100%;
        margin: auto !important;
        border: none !important;
        border-radius: 12px !important;
        box-shadow: none !important;
        padding: 10px !important;
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
    }
    
    /* Browse button in file uploader */
    [data-testid="stFileUploaderDropzone"] button {
        background: #00bf8f !important; /* Green color */
        color: transparent !important; /* Make original text transparent */
        border: none !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        font-size: 0 !important; /* Hide the original text */
        width: 100% !important;
        padding: 12px 16px !important; /* Increased padding for consistent height */
        position: relative;
        height: 44px !important; /* Fixed height for all buttons */
    }
    
    [data-testid="stFileUploaderDropzone"] button::before {
        content: "BROWSE FILES";
        display: block;
        width: 100%;
        color: white !important;
        font-size: 0.85rem !important;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
    }
    
    [data-testid="stFileUploaderDropzone"] button:hover {
        background: #00a67a !important; /* Darker green on hover */
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2) !important;
    }
    
    [data-testid="stFileUploaderDropzoneInstructions"] {
        display: none !important;
    }
    
    /* Ensure all text in sidebar is white with high contrast */
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] div {
        color: white !important;
        text-shadow: 0px 1px 2px rgba(0,0,0,0.15);
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] h4, 
    [data-testid="stSidebar"] h5, 
    [data-testid="stSidebar"] h6 {
        color: white !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.2);
    }
    
    /* Make markdown text white in sidebar */
    [data-testid="stSidebar"] .stMarkdown p {
        color: white !important;
        text-shadow: 0px 1px 2px rgba(0,0,0,0.15);
        font-weight: 500;
    }
    
    /* File uploader text color */
    [data-testid="stFileUploader"] label {
        color: white !important;
        font-weight: 600 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    /* Success message in sidebar */
    [data-testid="stSidebar"] [data-testid="stAlert"] {
        background: rgba(255, 255, 255, 0.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        backdrop-filter: blur(5px);
        border-radius: 8px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    }
    
    [data-testid="stSidebar"] [data-testid="stAlert"] p {
        color: white !important;
        font-weight: 600 !important;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
    }
    
    /* Ensure sidebar horizontal separators stand out */
    [data-testid="stSidebar"] hr {
        border-color: white !important;
        opacity: 0.7 !important;
        margin: 1.5rem 0 !important;
    }
    
    /* Sidebar headers */
    [data-testid="stSidebar"] h2 {
        color: white !important;
        padding: 1rem 0;
        border-bottom: 2px solid rgba(255, 255, 255, 0.5);
        margin-bottom: 1rem;
        font-weight: 700 !important;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
        letter-spacing: 0.5px;
    }
    
    /* Number input in sidebar */
    [data-testid="stSidebar"] [data-testid="stNumberInput"] input {
        background: rgba(255, 255, 255, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.8) !important;
        color: #000000 !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Number input label */
    [data-testid="stSidebar"] [data-testid="stNumberInput"] label {
        color: white !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        margin-bottom: 6px !important;
    }

    /* Number input controls */
    [data-testid="stSidebar"] [data-testid="stNumberInput"] button {
        background: rgba(255, 255, 255, 0.3) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
    }

    /* Buttons in sidebar - general rule for main functional buttons only */
    [data-testid="stSidebar"] .stButton > button {
        background: #00bf8f !important; /* Green color */
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.2) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        width: 100% !important;
        margin-bottom: 0 !important;
        transform: scale(1);
        height: 44px !important; /* Fixed height for all buttons */
        padding: 12px 16px !important; /* Consistent padding */
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
        border-radius: 8px !important;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: #00a67a !important; /* Darker green on hover */
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.25) !important;
    }
    
    /* Special utility buttons - sidebar collapse and file remove */
    button[kind="header"],
    button[data-testid="baseButton-header"],
    button[data-testid="baseButton-secondaryFormSubmit"],
    div[data-testid="stFileUploader"] button[aria-label="Clear file selection"],
    button[aria-label="Clear file selection"] {
        background: transparent !important;
        background-color: transparent !important;
        background-image: none !important;
        border: none !important;
        box-shadow: none !important;
        color: white !important;
        width: auto !important;
        margin: 0 !important;
        padding: 0.25rem !important;
        transform: none !important;
    }
    
    /* Hover state for utility buttons */
    button[kind="header"]:hover,
    button[data-testid="baseButton-header"]:hover,
    button[data-testid="baseButton-secondaryFormSubmit"]:hover,
    div[data-testid="stFileUploader"] button[aria-label="Clear file selection"]:hover,
    button[aria-label="Clear file selection"]:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        background-color: rgba(255, 255, 255, 0.1) !important;
        background-image: none !important;
        transform: none !important;
    }

    /* Button container spacing */
    [data-testid="stSidebar"] .success-button {
        margin-bottom: 0 !important;
        margin-top: 10px !important;
    }
    
    [data-testid="stSidebar"] .info-button {
        margin-top: 0 !important;
        margin-bottom: 10px !important;
    }
    
    /* Fix for sidebar headers - override the incorrect settings */
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: white !important;
        font-weight: 600;
    }

    /* Cards */
    .card {
        background: var(--white);
        border-radius: 12px;
        border: 1px solid var(--gray-300);
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 3px 6px rgba(0,0,0,0.08);
        transition: all 0.3s cubic-bezier(0.165, 0.84, 0.44, 1);
    }

    .card:hover {
        box-shadow: 0 10px 25px rgba(0, 191, 143, 0.2);
        transform: translateY(-5px);
        border-color: rgba(0, 191, 143, 0.3);
    }

    .card h3, .card h4 {
        color: #000000 !important;
        margin-bottom: 1rem;
    }

    .card p {
        color: #000000 !important;
        font-size: 1.05rem;
    }

    .feature-card {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(145deg, rgba(0, 191, 143, 0.05), rgba(0, 191, 143, 0.1));
        border: 1px solid var(--gray-300);
        border-radius: 10px;
        transition: all 0.4s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0, 191, 143, 0.2);
        border-color: rgba(0, 191, 143, 0.4);
    }
    
    .feature-card h4 {
        color: #000000 !important;
        margin: 1rem 0;
        font-size: 1.3rem;
    }
    
    .feature-card p {
        color: #000000 !important;
        font-size: 1.05rem;
    }

    /* Buttons */
    .stButton > button {
        color: white !important;
        border: none !important;
        padding: 0.6rem 1.2rem !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        font-size: 0.95rem !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15) !important;
    }

    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        background: transparent !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #000000 !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #000000 !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
    }
    
    /* DataFrames */
    .dataframe {
        border: 1px solid var(--gray-300) !important;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .dataframe:hover {
        box-shadow: 0 4px 12px rgba(0, 191, 143, 0.15);
    }
    
    .dataframe th {
        background-color: rgba(0, 191, 143, 0.1) !important;
        color: #000000 !important;
        font-weight: 600 !important;
        padding: 1rem !important;
        border-bottom: 2px solid rgba(0, 191, 143, 0.2) !important;
        font-size: 1.05rem !important;
    }
    
    .dataframe td {
        color: #000000 !important;
        padding: 0.75rem !important;
        border-bottom: 1px solid var(--gray-200) !important;
        background-color: var(--white) !important;
        transition: background-color 0.2s ease;
        font-size: 1.05rem !important;
    }
    
    .dataframe tr:hover td {
        background-color: rgba(0, 191, 143, 0.05) !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: var(--white);
        padding: 0.5rem;
        border-radius: 8px;
        border: 1px solid var(--gray-200);
    }

    .stTabs [data-baseweb="tab"] {
        background-color: var(--white) !important;
        color: #000000 !important;
        border: 1px solid var(--gray-200) !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        margin-right: 4px;
        font-size: 1.05rem !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(0, 191, 143, 0.1) !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 191, 143, 0.1) !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(120deg, var(--primary), var(--primary-dark)) !important;
        color: white !important;
        border-color: transparent !important;
        box-shadow: 0 4px 10px rgba(0, 191, 143, 0.3) !important;
    }

    /* Tab Colors - different for each tab */
    .stTabs [data-baseweb="tab"][aria-selected="true"] span,
    .stTabs [data-baseweb="tab"][aria-selected="true"] i {
        color: white !important;
    }
    
    .stTabs [data-baseweb="tab"] span,
    .stTabs [data-baseweb="tab"] i {
        color: inherit !important;
    }
    
    .stTabs [data-baseweb="tab"]:nth-of-type(1) {
        border-color: var(--info) !important;
        color: #000000 !important;
    }

    .stTabs [data-baseweb="tab"]:nth-of-type(1):hover,
    .stTabs [data-baseweb="tab"]:nth-of-type(1)[aria-selected="true"] {
        background: linear-gradient(120deg, var(--info), #1395a8) !important;
        color: white !important;
        border-color: transparent !important;
        box-shadow: 0 4px 10px rgba(23, 162, 184, 0.3) !important;
    }

    .stTabs [data-baseweb="tab"]:nth-of-type(2) {
        border-color: var(--success) !important;
        color: #000000 !important;
    }

    .stTabs [data-baseweb="tab"]:nth-of-type(2):hover,
    .stTabs [data-baseweb="tab"]:nth-of-type(2)[aria-selected="true"] {
        background: linear-gradient(120deg, var(--success), #218838) !important;
        color: white !important;
        border-color: transparent !important;
        box-shadow: 0 4px 10px rgba(40, 167, 69, 0.3) !important;
    }

    .stTabs [data-baseweb="tab"]:nth-of-type(3) {
        border-color: var(--warning) !important;
        color: #000000 !important;
    }

    .stTabs [data-baseweb="tab"]:nth-of-type(3):hover,
    .stTabs [data-baseweb="tab"]:nth-of-type(3)[aria-selected="true"] {
        background: linear-gradient(120deg, var(--warning), #e0a800) !important;
        color: white !important;
        border-color: transparent !important;
        box-shadow: 0 4px 10px rgba(255, 193, 7, 0.3) !important;
    }

    .stTabs [data-baseweb="tab"]:nth-of-type(4) {
        border-color: var(--purple) !important;
        color: #000000 !important;
    }

    .stTabs [data-baseweb="tab"]:nth-of-type(4):hover,
    .stTabs [data-baseweb="tab"]:nth-of-type(4)[aria-selected="true"] {
        background: linear-gradient(120deg, var(--purple), #5a35a0) !important;
        color: white !important;
        border-color: transparent !important;
        box-shadow: 0 4px 10px rgba(111, 66, 193, 0.3) !important;
    }

    /* Progress Bar */
    .stProgress > div > div {
        background: #00bf8f !important;
    }

    /* Info Boxes with different accent colors */
    .info-box {
        background: linear-gradient(to right, rgba(23, 162, 184, 0.05), white) !important;
        border-left: 4px solid var(--info);
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
        color: #000000 !important;
        animation: slideIn 0.5s ease-out;
        font-size: 1.05rem;
    }

    .success-box {
        background: linear-gradient(to right, rgba(40, 167, 69, 0.05), rgba(40, 167, 69, 0.1)) !important;
        border-left: 4px solid var(--success);
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
        color: #000000 !important;
        animation: slideIn 0.5s ease-out;
        font-size: 1.05rem;
    }
    
    .warning-box {
        background: linear-gradient(to right, rgba(255, 193, 7, 0.05), white) !important;
        border-left: 4px solid var(--warning);
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
        color: #000000 !important;
        animation: slideIn 0.5s ease-out;
        font-size: 1.05rem;
    }
    
    .danger-box {
        background: linear-gradient(to right, rgba(220, 53, 69, 0.05), white) !important;
        border-left: 4px solid var(--danger);
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
        color: #000000 !important;
        animation: slideIn 0.5s ease-out;
        font-size: 1.05rem;
    }

    /* Feature cards with different colors */
    .feature-card-success {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(145deg, rgba(40, 167, 69, 0.05), rgba(40, 167, 69, 0.1));
        border: 1px solid var(--gray-300);
        border-radius: 10px;
        transition: all 0.4s ease;
    }
    
    .feature-card-success:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(40, 167, 69, 0.2);
        border-color: rgba(40, 167, 69, 0.4);
    }
    
    .feature-card-info {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(145deg, rgba(23, 162, 184, 0.05), rgba(23, 162, 184, 0.1));
        border: 1px solid var(--gray-300);
        border-radius: 10px;
        transition: all 0.4s ease;
    }
    
    .feature-card-info:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(23, 162, 184, 0.2);
        border-color: rgba(23, 162, 184, 0.4);
    }
    
    .feature-card-warning {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(145deg, rgba(255, 193, 7, 0.05), rgba(255, 193, 7, 0.1));
        border: 1px solid var(--gray-300);
        border-radius: 10px;
        transition: all 0.4s ease;
    }
    
    .feature-card-warning:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(255, 193, 7, 0.2);
        border-color: rgba(255, 193, 7, 0.4);
    }
    
    /* Button variants */
    .success-button .stButton > button {
        background: #00bf8f !important; /* Green color */
    }

    .success-button .stButton > button:hover {
        background: #00a67a !important; /* Darker green on hover */
        box-shadow: 0 7px 14px rgba(0, 191, 143, 0.3) !important;
    }
    
    .success-button .stButton > button:before {
        content: "" !important;
        margin-right: 0 !important;
    }

    .info-button .stButton > button {
        background: #00bf8f !important; /* Green color */
    }

    .info-button .stButton > button:hover {
        background: #00a67a !important; /* Darker green on hover */
        box-shadow: 0 7px 14px rgba(0, 191, 143, 0.3) !important;
    }
    
    .info-button .stButton > button:before {
        content: "" !important;
        margin-right: 0 !important;
    }

    /* Documentation */
    .doc-container p {
        font-size: 1.05rem;
        line-height: 1.6;
        color: #000000 !important;
    }

    /* Fix for Table Cells */
    table {
        color: #000000 !important;
        font-size: 1.05rem !important;
    }
    
    th, td {
        color: #000000 !important;
        font-size: 1.05rem !important;
    }
    
    /* Fix for small text in various places */
    small, .small {
        color: #000000 !important;
        font-size: 0.95rem !important;
    }
    
    /* Fix for selectbox and dropdown text */
    [data-baseweb="select"] {
        color: #000000 !important;
        font-size: 1.05rem !important;
    }
    
    /* Radio buttons text */
    [data-testid="stRadio"] label {
        color: #000000 !important;
        font-size: 1.05rem !important;
    }

    /* Tab icon styling */
    .stTabs [data-baseweb="tab"] i {
        margin-right: 8px;
        font-size: 1.1rem;
    }
    
    /* Make selected tab more prominent */
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        font-weight: 600 !important;
        transform: translateY(-2px);
    }

    /* Make text in selected tabs white */
    .stTabs [data-baseweb="tab"][aria-selected="true"],
    .stTabs [data-baseweb="tab"][aria-selected="true"] *,
    .stTabs [data-baseweb="tab"]:hover[aria-selected="true"],
    .stTabs [data-baseweb="tab"]:hover[aria-selected="true"] * {
        color: white !important;
    }

    /* Sidebar horizontal separators */
    [data-testid="stSidebar"] hr {
        border-color: #00bf8f !important;
        border-width: 1px !important;
        opacity: 0.5 !important;
        margin: 1.5rem 0 !important;
    }

    /* Make sidebar icons white */
    button[kind="header"] svg,
    [data-testid="stFileUploader"] [aria-label="Clear file selection"] svg {
        fill: white !important;
        color: white !important;
    }
    
    /* Ensure Font Awesome icons maintain proper colors */
    .fa, .fas, .far, .fab, .fa-solid, .fa-regular, .fa-brands {
        color: inherit !important;
    }
    
    .icon-info { color: var(--info) !important; }
    .icon-success { color: var(--success) !important; }
    .icon-warning { color: var(--warning) !important; }
    .icon-danger { color: var(--danger) !important; }
    .icon-orange { color: var(--orange) !important; }
    .icon-purple { color: var(--purple) !important; }
    .icon-teal { color: var(--teal) !important; }
    .icon-indigo { color: var(--indigo) !important; }
    
    /* Documentation section icons */
    .doc-container .fas,
    .doc-container .fa {
        color: #00bf8f !important;
        display: inline-block !important;
        margin-right: 8px !important;
        vertical-align: middle !important;
    }
    
    .doc-container h1 i {
        color: #00bf8f !important;
    }
    
    .doc-section .icon-box i {
        color: #00bf8f !important;
    }
    
    .feature-list i.fa-laptop-code,
    .feature-list i.fa-shield-alt,
    .feature-list i.fa-brain,
    .feature-list i.fa-flask,
    .feature-list i.fa-graduation-cap {
        color: #17a2b8 !important;
    }
    
    .feature-list i.fa-file-csv,
    .feature-list i.fa-database,
    .feature-list i.fa-tachometer-alt,
    .feature-list i.fa-project-diagram,
    .feature-list i.fa-text-width,
    .feature-list i.fa-exclamation-circle {
        color: #dc3545 !important;
    }
    
    .doc-container i.fa-lightbulb,
    .doc-container i.fa-chart-bar,
    .doc-container i.fa-bolt {
        color: #ffc107 !important;
    }
    
    /* Documentation section specific styles */
    .doc-section .icon-box {
        display: inline-block;
        margin-right: 10px;
        vertical-align: middle;
    }
    
    .doc-container h1,
    .doc-container h2,
    .doc-container h3 {
        display: inline-block;
        vertical-align: middle;
    }
    
    .feature-list li {
        display: flex !important;
        align-items: center !important;
        margin-bottom: 8px !important;
    }
    
    /* Add spacing between icons and text in feature lists */
    .feature-list li i {
        margin-right: 8px !important;
        width: 16px !important;
        text-align: center !important;
        font-size: 1.1rem !important;
    }
    
    /* Add spacing between titles and text in feature lists */
    .feature-list li strong {
        margin-right: 3px !important;
        font-weight: 600 !important;
    }

    /* Fix for sidebar headers - override the incorrect settings */
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: white !important;
        font-weight: 600;
    }
         
</style>

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
""", unsafe_allow_html=True)

# Initialize AI agent
model = GroqModel(
    'qwen-qwq-32b', provider=GroqProvider(api_key='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')
)
# model = GroqModel('llama-3.3-70b-versatile', api_key='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')
agent = Agent(model)

# Session state initialization
if 'generated_data' not in st.session_state:
    st.session_state.generated_data = None
if 'original_data' not in st.session_state:
    st.session_state.original_data = None
if 'data_stats' not in st.session_state:
    st.session_state.data_stats = None
if 'generation_time' not in st.session_state:
    st.session_state.generation_time = None
if 'is_generating' not in st.session_state:
    st.session_state.is_generating = False

async def generate_synthetic_data(df: pd.DataFrame, num_rows: int) -> pd.DataFrame:
    start_time = time.time()
    
    # Create detailed column info
    column_info = []
    for col in df.columns:
        example_values = df[col].dropna().sample(min(3, len(df[col].dropna()))).tolist()
        examples = ", ".join([str(val) for val in example_values])
        value_range = ""
        if pd.api.types.is_numeric_dtype(df[col]):
            value_range = f" [range: {df[col].min()} to {df[col].max()}]"
        column_info.append(f"{col}: {df[col].dtype}{value_range} (examples: {examples})")
    
    column_details = "\n".join(column_info)
    
    prompt = (
        f"Generate {num_rows} rows of synthetic data that closely resembles this dataset. "
        f"Maintain the same columns, data types, value distributions, and relationships between fields.\n\n"
        f"Column details:\n{column_details}\n\n"
        f"Return ONLY valid CSV data with correct delimiters and NO additional text."
    )
    
    response = await agent.run(prompt)
    
    try:
        csv_data = response.data.strip()
        # Remove any markdown code blocks if present
        if csv_data.startswith("```") and csv_data.endswith("```"):
            csv_data = csv_data[3:-3].strip()
        
        df_synthetic = pd.read_csv(StringIO(csv_data))
        
        # Ensure data types match original dataset
        for col in df.columns:
            if col in df_synthetic.columns:
                df_synthetic[col] = df_synthetic[col].astype(df[col].dtype, errors='ignore')
        
        # Calculate generation time
        st.session_state.generation_time = round(time.time() - start_time, 2)
        
        # Calculate basic statistics
        st.session_state.data_stats = {
            'num_rows': len(df_synthetic),
            'num_columns': len(df_synthetic.columns),
            'memory_usage': f"{round(df_synthetic.memory_usage(deep=True).sum() / 1024, 2)} KB"
        }
        
    except Exception as e:
        st.error(f"Error parsing generated data: {e}")
        return pd.DataFrame()
    
    return df_synthetic

# Main layout
st.markdown('<h1 class="main-header">SynthGen AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Generate high-quality synthetic data with AI</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## SynthGen Controls")
   
    
    uploaded_file = st.file_uploader(
        "Upload your CSV dataset", 
        type=["csv"],
        help="Upload a CSV file to generate synthetic data based on its structure and content."
    )
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.original_data = df
            st.success(f"✅ Loaded {df.shape[0]} rows and {df.shape[1]} columns")
            
            # Options for generation
            st.markdown("### Generation Options")
            num_rows = st.number_input(
                "Number of synthetic rows to generate",
                min_value=1,
                max_value=1000,
                value=min(len(df), 100),
                help="Specify how many rows of synthetic data to generate"
            )
            
            # Generate button - outside the expander
            st.markdown('<div class="success-button">', unsafe_allow_html=True)
            if st.button("Generate Data", use_container_width=True):
                st.session_state.is_generating = True
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Reset button - outside the expander
            st.markdown('<div class="info-button">', unsafe_allow_html=True)
            if st.button("Reset", use_container_width=True):
                st.session_state.original_data = None
                st.session_state.generated_data = None
                st.session_state.is_generating = False
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error loading file: {e}")
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    SynthGen AI uses advanced LLMs to create realistic 
    synthetic data that preserves the statistical properties
    of your original dataset while ensuring privacy.
    """)
    st.markdown("Version 1.0.0")

# Main content area with tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Upload", 
    "Results", 
    "Visualization", 
    "Documentation"
])

with tab1:
    if st.session_state.original_data is None:
        st.markdown(
            """
            <div class="card">
                <h3>Welcome to SynthGen AI!</h3>
                <p>Get started by uploading a CSV file in the sidebar.</p>
                <p>SynthGen will analyze your data and generate high-quality synthetic data that preserves the statistical properties of your original dataset.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Feature cards
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(
                """
                <div class="card feature-card-success">
                    <div class="feature-icon"><i class="fas fa-shield-alt icon-success"></i></div>
                    <h4>🔒 Privacy Preserving</h4>
                    <p>Generate synthetic data without exposing sensitive information from your original dataset.</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                """
                <div class="card feature-card-info">
                    <div class="feature-icon"><i class="fas fa-brain icon-info"></i></div>
                    <h4>🧠 AI-Powered</h4>
                    <p>Leverages state-of-the-art LLMs to understand and replicate data patterns.</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
        with col3:
            st.markdown(
                """
                <div class="card feature-card-warning">
                    <div class="feature-icon"><i class="fas fa-chart-line icon-warning"></i></div>
                    <h4>📈 Statistically Valid</h4>
                    <p>Maintains distributions and relationships present in your original data.</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
    else:
        st.subheader("Original Dataset Preview")
        
        # Dataset summary
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Rows", f"{st.session_state.original_data.shape[0]:,}")
        with col2:
            st.metric("Columns", st.session_state.original_data.shape[1])
        with col3:
            mem_usage = round(st.session_state.original_data.memory_usage(deep=True).sum() / 1024, 2)
            st.metric("Memory Usage", f"{mem_usage} KB")
        
        # Column information table
        st.markdown("### Column Information")
        col_info = []
        for col in st.session_state.original_data.columns:
            dtype = str(st.session_state.original_data[col].dtype)
            missing = st.session_state.original_data[col].isna().sum()
            missing_pct = round(missing / len(st.session_state.original_data) * 100, 2)
            unique = st.session_state.original_data[col].nunique()
            
            col_info.append({
                "Column": col,
                "Data Type": dtype,
                "Missing Values": f"{missing} ({missing_pct}%)",
                "Unique Values": unique
            })
        
        st.dataframe(pd.DataFrame(col_info), use_container_width=True)
        
        # Data preview
        with st.expander("Original Data Preview", expanded=True):
            st.dataframe(st.session_state.original_data.head(10), use_container_width=True)

with tab2:
    if st.session_state.is_generating:
        st.markdown("""
        <div class="card animate-fade-in">
            <h3><i class="fas fa-cogs"></i> Generating Synthetic Data</h3>
            <div class="loader"></div>
        </div>
        """, unsafe_allow_html=True)
        
        progress_bar = st.progress(0)
        status_container = st.empty()
        
        # Run the generation
        async def run_generation():
            stages = [
                {"progress": 25, "message": "<i class='fas fa-database'></i> Analyzing dataset structure..."},
                {"progress": 50, "message": "<i class='fas fa-sitemap'></i> Identifying patterns and relationships..."},
                {"progress": 75, "message": "<i class='fas fa-robot'></i> Generating synthetic records..."},
                {"progress": 90, "message": "<i class='fas fa-check-circle'></i> Finalizing and validating output..."}
            ]
            
            for stage in stages:
                progress_bar.progress(stage["progress"])
                status_container.markdown(f"""
                <div class="info-box">
                    {stage["message"]} <span class="loading-pulse">●●●</span>
                </div>
                """, unsafe_allow_html=True)
                await asyncio.sleep(1)
            
            # Generate data
            st.session_state.generated_data = await generate_synthetic_data(
                st.session_state.original_data, 
                num_rows
            )
            
            # Complete the progress
            progress_bar.progress(100)
            status_container.markdown("""
            <div class="success-box">
                <i class="fas fa-check-circle"></i> Synthetic data generation complete!
            </div>
            """, unsafe_allow_html=True)
            
            st.session_state.is_generating = False
            await asyncio.sleep(1)
            st.rerun()
        
        asyncio.run(run_generation())
    
    elif st.session_state.generated_data is not None:
        st.markdown("""
        <div class="card animate-fade-in">
            <h3><i class="fas fa-check-circle icon-success"></i> Generation Results</h3>
            <p>Your synthetic data has been successfully generated. You can preview and download it below.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Result metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Synthetic Rows", f"{st.session_state.data_stats['num_rows']:,}", 
                     delta=f"{st.session_state.data_stats['num_rows'] - len(st.session_state.original_data):,}" 
                     if st.session_state.data_stats['num_rows'] != len(st.session_state.original_data) else None)
        with col2:
            st.metric("Generation Time", f"{st.session_state.generation_time} seconds")
        with col3:
            st.metric("Memory Usage", st.session_state.data_stats['memory_usage'])
        
        # Results container
        st.markdown("""
        <div class="card">
            <h3><i class="fas fa-table icon-info"></i> Synthetic Data Preview</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.dataframe(st.session_state.generated_data, use_container_width=True)
        
        # Download options
        st.markdown("<h3><i class='fas fa-download icon-success'></i> Download Options</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            csv_data = st.session_state.generated_data.to_csv(index=False)
            st.download_button(
                "⬇Download CSV",
                csv_data,
                "synthetic_data.csv",
                "text/csv",
                use_container_width=True
            )
        with col2:
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                st.session_state.generated_data.to_excel(writer, index=False)
            st.download_button(
                "⬇Download Excel",
                buffer.getvalue(),
                "synthetic_data.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    else:
        st.markdown("""
        <div class="info-box">
            <i class="fas fa-info-circle icon-info"></i>&nbsp;&nbsp;Generate synthetic data to see results here.
        </div>
        """, unsafe_allow_html=True)

with tab3:
    if st.session_state.original_data is not None and st.session_state.generated_data is not None:
        st.markdown("""
        <div class="card">
            <h3><i class="fas fa-chart-bar icon-info"></i> Data Visualization</h3>
            <p>Compare the distribution of values between your original and synthetic datasets to evaluate the quality of generated data.</p>
            <p>Select different visualization types to understand how well the synthetic data preserves the statistical properties of your original dataset.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Column selector for visualization
        numeric_columns = [col for col in st.session_state.original_data.columns 
                         if pd.api.types.is_numeric_dtype(st.session_state.original_data[col])]
        
        if numeric_columns:
            # Add a nicer UI for column selection
            st.markdown("""
            <div class="card feature-card-info">
                <h4><i class="fas fa-columns icon-info"></i> Visualization Controls</h4>
                <p>Choose columns and visualization type to compare original and synthetic data distributions.</p>
            </div>
            """, unsafe_allow_html=True)
            
            selected_column = st.selectbox(
                "Select column to visualize",
                numeric_columns,
                format_func=lambda x: f"{x} (Numeric)"
            )
            
            # Add visualization type selector
            viz_type = st.radio(
                "Select visualization type",
                ["Histogram", "Box Plot", "Scatter Plot"],
                horizontal=True
            )
            
            st.markdown("""
            <div class="card">
                <h4><i class="fas fa-chart-line icon-success"></i> Data Comparison Visualizations</h4>
            </div>
            """, unsafe_allow_html=True)
            
            if viz_type == "Histogram":
                # Create two columns for side-by-side visualization
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.markdown(f"#### <i class='fas fa-chart-area icon-info'></i> Original Data", unsafe_allow_html=True)
                    fig1 = px.histogram(
                        st.session_state.original_data, 
                        x=selected_column,
                        title=f"Distribution of {selected_column} (Original)",
                        color_discrete_sequence=['#17a2b8'],
                        opacity=0.8,
                        template="plotly_white"
                    )
                    fig1.update_layout(
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                        margin=dict(l=20, r=20, t=40, b=20),
                    )
                    st.plotly_chart(fig1, use_container_width=True)
                    st.markdown("""
                    <p class="visualization-help">Original distribution showcases the actual data patterns</p>
                    """, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.markdown(f"#### <i class='fas fa-chart-area icon-success'></i> Synthetic Data", unsafe_allow_html=True)
                    fig2 = px.histogram(
                        st.session_state.generated_data, 
                        x=selected_column,
                        title=f"Distribution of {selected_column} (Synthetic)",
                        color_discrete_sequence=['#28a745'],
                        opacity=0.8,
                        template="plotly_white"
                    )
                    fig2.update_layout(
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                        margin=dict(l=20, r=20, t=40, b=20),
                    )
                    st.plotly_chart(fig2, use_container_width=True)
                    st.markdown("""
                    <p class="visualization-help">Synthetic distribution should mirror the original closely</p>
                    """, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                
            elif viz_type == "Box Plot":
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("#### <i class='fas fa-box icon-warning'></i> Distribution Comparison", unsafe_allow_html=True)
                
                # Create comparison dataframe
                orig_df = st.session_state.original_data[[selected_column]].copy()
                orig_df['Type'] = 'Original'
                
                synth_df = st.session_state.generated_data[[selected_column]].copy()
                synth_df['Type'] = 'Synthetic'
                
                combined_df = pd.concat([orig_df, synth_df])
                
                fig3 = px.box(
                    combined_df, 
                    x='Type', 
                    y=selected_column,
                    color='Type',
                    color_discrete_map={'Original': '#17a2b8', 'Synthetic': '#28a745'},
                    title=f"Distribution Comparison for {selected_column}",
                    template="plotly_white",
                    points="all"
                )
                fig3.update_layout(
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    margin=dict(l=20, r=20, t=40, b=20),
                )
                st.plotly_chart(fig3, use_container_width=True)
                st.markdown("""
                <p class="visualization-help">Box plots show the medians, quartiles, and outliers - similar patterns indicate good synthetic data quality</p>
                """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
            else:  # Scatter Plot
                # Only show if we have at least 2 numeric columns
                if len(numeric_columns) >= 2:
                    st.markdown("""
                    <div class="card feature-card-warning">
                        <h4><i class="fas fa-project-diagram icon-warning"></i> Relationship Analysis</h4>
                        <p>Select a second column to analyze relationships between variables in both datasets.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    second_column = st.selectbox(
                        "Select second column",
                        [col for col in numeric_columns if col != selected_column],
                        format_func=lambda x: f"{x} (Numeric)"
                    )
                    
                    # Create two columns for side-by-side visualization
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("<div class='card'>", unsafe_allow_html=True)
                        st.markdown(f"#### <i class='fas fa-dot-circle icon-info'></i> Original Data", unsafe_allow_html=True)
                        fig4 = px.scatter(
                            st.session_state.original_data, 
                            x=selected_column,
                            y=second_column,
                            title=f"Relationship: {selected_column} vs {second_column} (Original)",
                            color_discrete_sequence=['#17a2b8'],
                            template="plotly_white",
                            opacity=0.7
                        )
                        fig4.update_layout(
                            margin=dict(l=20, r=20, t=40, b=20),
                        )
                        st.plotly_chart(fig4, use_container_width=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("<div class='card'>", unsafe_allow_html=True)
                        st.markdown(f"#### <i class='fas fa-dot-circle icon-success'></i> Synthetic Data", unsafe_allow_html=True)
                        fig5 = px.scatter(
                            st.session_state.generated_data, 
                            x=selected_column,
                            y=second_column,
                            title=f"Relationship: {selected_column} vs {second_column} (Synthetic)",
                            color_discrete_sequence=['#28a745'],
                            template="plotly_white",
                            opacity=0.7
                        )
                        fig5.update_layout(
                            margin=dict(l=20, r=20, t=40, b=20),
                        )
                        st.plotly_chart(fig5, use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    st.markdown("""
                    <div class="card">
                        <p class="visualization-help">Scatter plots reveal relationships between variables - similar patterns indicate the synthetic data preserves variable correlations</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="danger-box">
                        <i class="fas fa-exclamation-circle icon-danger" style="font-size: 24px;"></i>
                        <h4>Additional Column Needed</h4>
                        <p>To create scatter plots, you need at least 2 numeric columns in your dataset. Please upload a dataset with multiple numeric columns to use this visualization.</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Add statistics comparison
            st.markdown("""
            <div class="card feature-card-success">
                <h4><i class="fas fa-calculator icon-success"></i> Statistical Analysis</h4>
                <p>Compare key statistical measures between original and synthetic data to evaluate how well the statistical properties are preserved.</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("##### <i class='fas fa-table icon-info'></i> Original Data Statistics", unsafe_allow_html=True)
                stats_orig = st.session_state.original_data[selected_column].describe().to_frame().T
                st.dataframe(stats_orig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("##### <i class='fas fa-table icon-success'></i> Synthetic Data Statistics", unsafe_allow_html=True)
                stats_synth = st.session_state.generated_data[selected_column].describe().to_frame().T
                st.dataframe(stats_synth, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="danger-box">
                <i class="fas fa-exclamation-triangle icon-danger" style="font-size: 24px;"></i>
                <h4>No Numeric Columns Found</h4>
                <p>To visualize data distributions and relationships, your dataset needs to contain numeric columns. Please upload a dataset with numeric data to use these visualization tools.</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="card">
            <h3><i class="fas fa-chart-bar icon-orange"></i> Data Visualization</h3>
            <p>This tab allows you to visually compare your original data with the generated synthetic data.</p>
            <p>Various visualization options will help you assess how well the synthetic data preserves the statistical properties of your original dataset.</p>
        </div>
        
        <div class="card">
            <div class="empty-card-hint">
                <i class="fas fa-database icon-purple" style="font-size: 48px;"></i>
                <h4>No Data Available Yet</h4>
                <p>Upload a CSV file and generate synthetic data to enable visualizations.</p>
            </div>
        </div>
        
        <div class="card">
            <h4>Available Visualization Types</h4>
            <ul class="feature-list">
                <li><i class="fas fa-chart-area icon-info"></i>&nbsp;<strong>Histograms:</strong>&nbsp; Compare distribution shapes between original and synthetic data</li>
                <li><i class="fas fa-box icon-warning"></i>&nbsp;<strong>Box Plots:</strong>&nbsp; Compare medians, quartiles, and outliers</li>
                <li><i class="fas fa-project-diagram icon-success"></i>&nbsp;<strong>Scatter Plots:</strong>&nbsp; Verify that correlations between variables are preserved</li>
                <li><i class="fas fa-calculator icon-danger"></i>&nbsp;<strong>Statistical Analysis:</strong>&nbsp; Compare key statistical measures side-by-side</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
with tab4:
    st.markdown("""
    <div class="doc-container">
        <h1 style="display: flex; align-items: center;"><i class="fas fa-database icon-info"></i>&nbsp;SynthGen AI Documentation</h1>
        <div class="doc-section">
           <span style="display: inline-flex; align-items: center;"><i class="fas fa-globe icon-info"></i>&nbsp;<h2>Overview</h2></span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    SynthGen AI is a powerful tool that generates high-quality synthetic data based on your original dataset. The synthetic data maintains the statistical properties found in your original data while ensuring privacy and confidentiality.
    
    Using advanced Large Language Models (LLMs), SynthGen can analyze the structure and patterns in your data to create realistic synthetic versions that can be used for testing and development without exposing sensitive information.
    
    Our tool is designed to be user-friendly while providing enterprise-grade synthetic data generation capabilities. Whether you're a data scientist, developer, or business analyst, SynthGen AI helps you create realistic test data without compromising privacy or security.
    """)
    
    st.markdown("""
    <div class="doc-section">
        <span style="display: inline-flex; align-items: center;"><i class="fas fa-map-signs icon-info"></i>&nbsp;<h2>How to Use</h2></span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <table style="width:100%; border-collapse: collapse;">
        <tr>
            <td style="width:50px; vertical-align:top; padding-bottom:12px;"><i class="fas fa-file-upload icon-info"></i></td>
            <td style="width:150px; vertical-align:top; font-weight:bold; padding-bottom:12px;">Upload Data:</td>
            <td style="vertical-align:top; padding-bottom:12px;">Start by uploading your CSV file using the uploader in the sidebar. SynthGen will analyze the structure and content of your data.</td>
        </tr>
        <tr>
            <td style="width:50px; vertical-align:top; padding-bottom:12px;"><i class="fas fa-sliders-h icon-info"></i></td>
            <td style="width:150px; vertical-align:top; font-weight:bold; padding-bottom:12px;">Configure Options:</td>
            <td style="vertical-align:top; padding-bottom:12px;">Set the number of rows you wish to generate in the synthetic dataset.</td>
        </tr>
        <tr>
            <td style="width:50px; vertical-align:top; padding-bottom:12px;"><i class="fas fa-magic icon-info"></i></td>
            <td style="width:150px; vertical-align:top; font-weight:bold; padding-bottom:12px;">Generate Data:</td>
            <td style="vertical-align:top; padding-bottom:12px;">Click the "Generate Synthetic Data" button to start the generation process.</td>
        </tr>
        <tr>
            <td style="width:50px; vertical-align:top; padding-bottom:12px;"><i class="fas fa-clipboard-check icon-info"></i></td>
            <td style="width:150px; vertical-align:top; font-weight:bold; padding-bottom:12px;">Explore Results:</td>
            <td style="vertical-align:top; padding-bottom:12px;">View and download your synthetic data from the Results tab.</td>
        </tr>
        <tr>
            <td style="width:50px; vertical-align:top; padding-bottom:12px;"><i class="fas fa-chart-line icon-info"></i></td>
            <td style="width:150px; vertical-align:top; font-weight:bold; padding-bottom:12px;">Visualize:</td>
            <td style="vertical-align:top; padding-bottom:12px;">Compare the original and synthetic data distributions in the Visualization tab.</td>
        </tr>
    </table>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="doc-section">
            <span style="display: inline-flex; align-items: center;"><i class="fas fa-tasks icon-success"></i>&nbsp;<h2>Use Cases</h2></span>
        </div>
        <table style="width:100%; border-collapse: collapse;">
            <tr>
                <td style="width:50px; vertical-align:top; padding-bottom:12px;"><i class="fas fa-laptop-code icon-info"></i></td>
                <td style="width:150px; vertical-align:top; font-weight:bold; padding-bottom:12px;">Development & Testing:</td>
                <td style="vertical-align:top; padding-bottom:12px;">Use synthetic data to test applications without compromising real user data</td>
            </tr>
            <tr>
                <td style="width:50px; vertical-align:top; padding-bottom:12px;"><i class="fas fa-shield-alt icon-info"></i></td>
                <td style="width:150px; vertical-align:top; font-weight:bold; padding-bottom:12px;">Privacy Compliance:</td>
                <td style="vertical-align:top; padding-bottom:12px;">Train AI models while complying with GDPR, HIPAA, and other regulations</td>
            </tr>
            <tr>
                <td style="width:50px; vertical-align:top; padding-bottom:12px;"><i class="fas fa-brain icon-info"></i></td>
                <td style="width:150px; vertical-align:top; font-weight:bold; padding-bottom:12px;">Machine Learning:</td>
                <td style="vertical-align:top; padding-bottom:12px;">Generate additional training data for machine learning models</td>
            </tr>
            <tr>
                <td style="width:50px; vertical-align:top; padding-bottom:12px;"><i class="fas fa-flask icon-info"></i></td>
                <td style="width:150px; vertical-align:top; font-weight:bold; padding-bottom:12px;">Research:</td>
                <td style="vertical-align:top; padding-bottom:12px;">Share datasets without revealing confidential information</td>
            </tr>
            <tr>
                <td style="width:50px; vertical-align:top; padding-bottom:12px;"><i class="fas fa-graduation-cap icon-info"></i></td>
                <td style="width:150px; vertical-align:top; font-weight:bold; padding-bottom:12px;">Education:</td>
                <td style="vertical-align:top; padding-bottom:12px;">Create realistic datasets for educational purposes</td>
            </tr>
        </table>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="doc-section">
            <span style="display: inline-flex; align-items: center;"><i class="fas fa-exclamation-circle icon-danger"></i>&nbsp;<h2>Limitations</h2></span>
        </div>
        <table style="width:100%; border-collapse: collapse;">
            <tr>
                <td style="width:50px; vertical-align:top; padding-bottom:12px;"><i class="fas fa-file-csv icon-danger"></i></td>
                <td style="width:150px; vertical-align:top; font-weight:bold; padding-bottom:12px;">File Format:</td>
                <td style="vertical-align:top; padding-bottom:12px;">Currently supports CSV files only</td>
            </tr>
            <tr>
                <td style="width:50px; vertical-align:top; padding-bottom:12px;"><i class="fas fa-database icon-danger"></i></td>
                <td style="width:150px; vertical-align:top; font-weight:bold; padding-bottom:12px;">Data Size:</td>
                <td style="vertical-align:top; padding-bottom:12px;">Limited to processing up to 10,000 rows</td>
            </tr>
            <tr>
                <td style="width:50px; vertical-align:top; padding-bottom:12px;"><i class="fas fa-tachometer-alt icon-danger"></i></td>
                <td style="width:150px; vertical-align:top; font-weight:bold; padding-bottom:12px;">Performance:</td>
                <td style="vertical-align:top; padding-bottom:12px;">Large datasets may require more processing time</td>
            </tr>
            <tr>
                <td style="width:50px; vertical-align:top; padding-bottom:12px;"><i class="fas fa-project-diagram icon-danger"></i></td>
                <td style="width:150px; vertical-align:top; font-weight:bold; padding-bottom:12px;">Complex Relationships:</td>
                <td style="vertical-align:top; padding-bottom:12px;">May not preserve complex inter-column relationships perfectly</td>
            </tr>
            <tr>
                <td style="width:50px; vertical-align:top; padding-bottom:12px;"><i class="fas fa-text-width icon-danger"></i></td>
                <td style="width:150px; vertical-align:top; font-weight:bold; padding-bottom:12px;">Text Generation:</td>
                <td style="vertical-align:top; padding-bottom:12px;">Long text fields may not maintain perfect semantic meaning</td>
            </tr>
        </table>
        """, unsafe_allow_html=True)
        
        st.markdown("""
    <div class="doc-section">
            <span style="display: inline-flex; align-items: center;"><i class="fas fa-lightbulb icon-warning"></i>&nbsp;<h2>Advanced Features & Tips</h2></span>
        </div>
        """, unsafe_allow_html=True)
        
        # Statistical Preservation and Performance Tips in a single table
        st.markdown("""
        <table style="width:100%; border-collapse: collapse;">
            <tr>
                <td style="width:50px; vertical-align:top; padding-bottom:12px;"><i class="fas fa-chart-bar icon-success"></i></td>
                <td style="width:150px; vertical-align:top; font-weight:bold; padding-bottom:12px;">Statistical Preservation:</td>
                <td style="vertical-align:top; padding-bottom:12px;">SynthGen AI maintains key statistical properties including:
                    <ul style="margin-top:8px; margin-left:0px; padding-left:20px;">
                        <li>Mean, median, and mode values</li>
                        <li>Standard deviation and variance</li>
                        <li>Correlations between columns</li>
                        <li>Distribution shapes</li>
                    </ul>
                </td>
            </tr>
            <tr>
                <td style="width:50px; vertical-align:top; padding-bottom:12px;"><i class="fas fa-bolt icon-warning"></i></td>
                <td style="width:150px; vertical-align:top; font-weight:bold; padding-bottom:12px;">Performance Tips:</td>
                <td style="vertical-align:top; padding-bottom:12px;">
                    <ul style="margin-top:8px; margin-left:0px; padding-left:20px;">
                        <li>For faster results, limit your dataset to the most essential columns</li>
                        <li>Consider using a sample of very large datasets</li>
                        <li>Complex numerical relationships are better preserved than text relationships</li>
                    </ul>
                </td>
            </tr>
        </table>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 40px; padding: 20px;">
        <p>SynthGen AI - Version 1.0.0</p>
        <p>Built with <i class="fas fa-heart" style="color: #FF4081;"></i> using Streamlit and LLM Technology</p>
    </div>
    """, unsafe_allow_html=True) 

if __name__ == "__main__":
    # This is a no-op for Streamlit as it handles its own server
    # But it's a good practice to include for local development and other frameworks
    pass


