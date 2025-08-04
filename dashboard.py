import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Disaster Law Protections Across Regions")

# Correct file path
DATA_PATH = "Final_Combined_Emergency_Law_Data.csv"

@st.cache_data
def load_data(path):
    return pd.read_csv(path)

# Check file exists
import os
if not os.path.exists(DATA_PATH):
    st.error(f"⚠️ File not found: {DATA_PATH}. Make sure it's in the app folder.")
    st.stop()

# Load the data
df = load_data(DATA_PATH)

# Define columns to visualize
feature_columns = [
    'Vulnerable Populations Protections',
    'Local Authority',
    'Emergency Declaration',
    'Mitigation Planning',
    'Mutual Aid',
    'Equity Initiatives'
]

# Filter to actual columns in the dataset
valid_columns = [col for col in feature_columns if col in df.columns]

# Show data preview
with st.expander("🔍 Preview Raw Data"):
    st.dataframe(df[valid_columns + ['SourceFile']] if 'SourceFile' in df.columns else df[valid_columns])

# Bar charts for each column
st.subheader("🧭 Feature Presence Across Jurisdictions")
cols = st.columns(3)
for i, col in enumerate(valid_columns):
    with cols[i % 3]:
        fig, ax = plt.subplots(figsize=(5, 4))
        sns.countplot(data=df, x=col, order=df[col].dropna().unique(), ax=ax)
        ax.set_title(col)
        ax.set_xlabel("")
        ax.set_ylabel("Count")
        plt.xticks(rotation=45)
        st.pyplot(fig)

# Optional region filter
if 'Region' in df.columns:
    st.subheader("📍 Explore by Region")
    region = st.selectbox("Select a Region", options=df['Region'].dropna().unique())
    st.dataframe(df[df['Region'] == region][valid_columns + ['Region']])
