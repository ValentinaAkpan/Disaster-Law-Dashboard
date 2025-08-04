import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(page_title="Disaster Law Dashboard", layout="wide")
st.title("📘 Disaster Law Dashboard for US States")

# Load data
DATA_PATH = "Final_Combined_Emergency_Law_Data.csv"

@st.cache_data
def load_data(path):
    return pd.read_csv(path)

df = load_data(DATA_PATH)
df.columns = [col.strip() for col in df.columns]  # Clean column names

# Sidebar filter with "All States"
st.sidebar.header("🧭 Filter Options")

all_states = sorted(df["State"].dropna().unique())
state_options = ["All States"] + all_states
selected_state = st.sidebar.selectbox("Select a State", state_options)

# Filter logic
if selected_state == "All States":
    filtered_df = df.copy()
else:
    filtered_df = df[df["State"] == selected_state]

# Bar Chart: Number of entries per state
st.subheader("📌 Number of Entries per State")
state_count = df["State"].value_counts().reset_index()
state_count.columns = ["State", "Count"]
fig_bar = px.bar(state_count, x="State", y="Count", title="Number of Entries per State")
st.plotly_chart(fig_bar, use_container_width=True)

# Pie Chart: Local Authority Enabled
st.subheader("🏛️ Local Authority Enabled (Yes/No)")
authority_count = filtered_df["Local Authority"].value_counts().reset_index()
authority_count.columns = ["Response", "Count"]
fig_pie = px.pie(authority_count, names="Response", values="Count", title="Local Authority Status")
st.plotly_chart(fig_pie, use_container_width=True)

# Optional: Protections summary per state
if "Vulnerable Populations Protections" in filtered_df.columns:
    protection_counts = (
        filtered_df["Vulnerable Populations Protections"]
        .value_counts()
        .reset_index()
    )
    protection_counts.columns = ["Protection", "Count"]
    if not protection_counts.empty:
        st.subheader("👥 Vulnerable Populations Protections")
        fig_protect = px.bar(
            protection_counts,
            x="Protection",
            y="Count",
            title="Protections in Selected State"
        )
        st.plotly_chart(fig_protect, use_container_width=True)
