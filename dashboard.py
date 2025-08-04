import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(page_title="Disaster Law Dashboard", layout="wide")
st.title("📘 Disaster Law Dashboard for US States")

# Load CSV file
DATA_PATH = "Final_Combined_Emergency_Law_Data.csv"

@st.cache_data
def load_data(path):
    return pd.read_csv(path)

df = load_data(DATA_PATH)
df.columns = [col.strip() for col in df.columns]  # Clean column names

# Sidebar filter with "All States" option
st.sidebar.header("🧭 Filter Options")
all_states = sorted(df["State"].dropna().unique())
state_options = ["All States"] + all_states
selected_state = st.sidebar.selectbox("Select a State", state_options)

# Filter logic
if selected_state == "All States":
    filtered_df = df.copy()
else:
    filtered_df = df[df["State"] == selected_state]

# -------------------------
# 📈 Metrics Overview
# -------------------------
st.subheader("📈 Metrics Overview")

col_a, col_b, col_c, col_d = st.columns(4)

def count_yes(column):
    if column in filtered_df.columns:
        return filtered_df[column].str.lower().eq("yes").sum()
    return 0

with col_a:
    st.metric("Equity Initiatives", count_yes("Equity Initiatives"))

with col_b:
    st.metric("Mutual Aid Agreements", count_yes("Mutual Aid"))

with col_c:
    st.metric("Mitigation Planning", count_yes("Mitigation Planning"))

with col_d:
    st.metric("Emergency Powers (Local)", count_yes("Local Emergency Powers"))

# 📌 Bar Chart: Number of entries (filtered)
st.subheader("📌 Number of Entries per State")
state_count = filtered_df["State"].value_counts().reset_index()
state_count.columns = ["State", "Count"]
fig_bar = px.bar(
    state_count,
    x="State",
    y="Count",
    title="Number of Entries" if selected_state != "All States" else "Number of Entries per State"
)
st.plotly_chart(fig_bar, use_container_width=True)

# 🏛️ Pie Chart: Local Authority Enabled (Yes/No)
st.subheader("🏛️ Local Authority Enabled (Yes/No)")
if "Local Authority" in filtered_df.columns:
    authority_count = filtered_df["Local Authority"].value_counts().reset_index()
    authority_count.columns = ["Response", "Count"]
    fig_pie = px.pie(
        authority_count,
        names="Response",
        values="Count",
        title="Local Authority Status"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# 👥 Protections bar chart
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
            title="Protections in Selected State" if selected_state != "All States" else "Protections Across All States"
        )
        st.plotly_chart(fig_protect, use_container_width=True)

# 🟣 Pie Chart: Equity Initiatives
if "Equity Initiatives" in filtered_df.columns:
    equity_counts = filtered_df["Equity Initiatives"].value_counts().reset_index()
    equity_counts.columns = ["Response", "Count"]
    fig_equity = px.pie(
        equity_counts,
        names="Response",
        values="Count",
        title="Equity Initiatives"
    )
    st.plotly_chart(fig_equity, use_container_width=True)

# 🔵 Pie Chart: Mitigation Planning
if "Mitigation Planning" in filtered_df.columns:
    mitigation_counts = filtered_df["Mitigation Planning"].value_counts().reset_index()
    mitigation_counts.columns = ["Response", "Count"]
    fig_mitigation = px.pie(
        mitigation_counts,
        names="Response",
        values="Count",
        title="Mitigation Planning"
    )
    st.plotly_chart(fig_mitigation, use_container_width=True)
