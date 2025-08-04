import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Disaster Law Dashboard", layout="wide")
st.title("📊 Disaster Law Protections Across Regions")

# Load CSV file
DATA_PATH = "Final_Combined_Emergency_Law_Data.csv"

@st.cache_data
def load_data(path):
    return pd.read_csv(path)

df = load_data(DATA_PATH)

# Clean and prep
df.columns = [col.strip() for col in df.columns]
feature_columns = [
    'Vulnerable Populations Protections',
    'Local Authority',
    'Emergency Declaration',
    'Mitigation Planning',
    'Mutual Aid',
    'Equity Initiatives'
]
valid_columns = [col for col in feature_columns if col in df.columns]

# Sidebar filters
st.sidebar.header("🔎 Filter Data")
region_filter = st.sidebar.multiselect(
    "Select Region(s)", 
    options=sorted(df['Region'].dropna().unique()), 
    default=sorted(df['Region'].dropna().unique())
)

feature_filters = {}
for col in valid_columns:
    values = sorted(df[col].dropna().unique())
    if values:
        feature_filters[col] = st.sidebar.multiselect(f"{col}", values, default=values)

# Apply filters
filtered_df = df[df['Region'].isin(region_filter)]
for col, values in feature_filters.items():
    if values:
        filtered_df = filtered_df[filtered_df[col].isin(values)]

# Show filtered table
st.subheader("📋 Filtered Data")
st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)

# Count plots for each feature
st.subheader("📈 Feature Presence (Filtered)")

plot_cols = st.columns(3)
for i, col in enumerate(valid_columns):
    with plot_cols[i % 3]:
        fig, ax = plt.subplots(figsize=(5, 4))
        sns.countplot(data=filtered_df, x=col, order=filtered_df[col].dropna().unique(), ax=ax)
        ax.set_title(col)
        ax.set_xlabel("")
        ax.set_ylabel("Count")
        plt.xticks(rotation=45)
        st.pyplot(fig)
