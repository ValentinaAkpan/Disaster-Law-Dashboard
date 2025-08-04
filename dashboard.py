import streamlit as st
import pandas as pd
import plotly.express as px

# Page settings
st.set_page_config(page_title="Disaster Law Dashboard", layout="wide")
st.title("📘 Disaster Law Dashboard for US States")

# Load data
DATA_PATH = "Final_Combined_Emergency_Law_Data.csv"

@st.cache_data
def load_data(path):
    return pd.read_csv(path)

df = load_data(DATA_PATH)
df.columns = [col.strip() for col in df.columns]  # Clean column names

# Basic Metrics
st.subheader("📊 Basic Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Unique States", df["State"].nunique())

with col2:
    st.metric("Local Authority Enabled", df['Local Authority'].str.lower().eq("yes").sum())

with col3:
    st.metric("Has Vulnerable Populations Protections", df["Vulnerable Populations Protections"].notna().sum())

# Bar Chart: Number of laws per state
st.subheader("📌 Number of Entries per State")
state_count = df["State"].value_counts().reset_index()
state_count.columns = ["State", "Count"]
fig_bar = px.bar(state_count, x="State", y="Count", title="Number of Entries per State")
st.plotly_chart(fig_bar, use_container_width=True)

# Pie Chart: Local Authority Enabled
st.subheader("🏛️ Local Authority Enabled (Yes/No)")
authority_count = df["Local Authority"].value_counts().reset_index()
authority_count.columns = ["Response", "Count"]
fig_pie = px.pie(authority_count, names="Response", values="Count", title="Local Authority Enabled")
st.plotly_chart(fig_pie, use_container_width=True)

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

st.subheader(f"📄 Data for **{selected_state}**")

if filtered_df.empty:
    st.warning("No data available for selected state.")
else:
    st.dataframe(filtered_df)

    # Optional: Breakdown of protections for selected state
    if "Vulnerable Populations Protections" in filtered_df.columns:
        protection_counts = (
            filtered_df["Vulnerable Populations Protections"]
            .value_counts()
            .reset_index()
        )
        protection_counts.columns = ["Protection", "Count"]
        if not protection_counts.empty:
            st.markdown("**Protection Summary**")
            fig_protect = px.bar(
                protection_counts,
                x="Protection",
                y="Count",
                title="Protections in Selected State"
            )
            st.plotly_chart(fig_protect, use_container_width=True)

# Download button
st.download_button(
    label="⬇️ Download Filtered Data as CSV",
    data=filtered_df.to_csv(index=False),
    file_name=f"{selected_state.replace(' ', '_')}_disaster_laws.csv",
    mime="text/csv"
)
