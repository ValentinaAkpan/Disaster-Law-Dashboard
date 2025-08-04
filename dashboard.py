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
df.columns = [col.strip() for col in df.columns]

# Top filter
st.markdown("### 🔍 Filter by State")
all_states = sorted(df["State"].dropna().unique())
state_options = ["All States"] + all_states
selected_state = st.selectbox("Select a State", state_options, index=0)

# Filter logic
filtered_df = df if selected_state == "All States" else df[df["State"] == selected_state]

# Helper for metrics
def count_yes(column):
    return filtered_df[column].str.lower().eq("yes").sum() if column in filtered_df.columns else 0

# Tab styling
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab"] {
        font-weight: 700 !important;
        font-size: 18px !important;
        padding: 1rem 2rem !important;
        margin-right: 1rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["📈 Metrics", "📌 State Charts", "🛡️ Protections"])

with tab1:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Equity Initiatives", count_yes("Equity Initiatives"))
    col2.metric("Mutual Aid Agreements", count_yes("Mutual Aid"))
    col3.metric("Mitigation Planning", count_yes("Mitigation Planning"))
    col4.metric("Emergency Powers (Local)", count_yes("Local Emergency Powers"))

with tab2:
    st.subheader("📌 Number of Entries per State")
    state_count = filtered_df["State"].value_counts().reset_index()
    state_count.columns = ["State", "Count"]
    fig_bar = px.bar(state_count, x="State", y="Count", title="Entries per State")
    st.plotly_chart(fig_bar, use_container_width=True)

    if "Local Authority" in filtered_df.columns:
        st.subheader("🏛️ Local Authority Enabled")
        authority_count = filtered_df["Local Authority"].value_counts().reset_index()
        authority_count.columns = ["Response", "Count"]
        fig_pie = px.pie(authority_count, names="Response", values="Count", title="Local Authority Status")
        st.plotly_chart(fig_pie, use_container_width=True)

with tab3:
    def simplify_protection(val):
        val = str(val).lower()
        if "language" in val:
            return "Language Access"
        elif "disability" in val or "functional need" in val:
            return "Disability Inclusion"
        elif "equity" in val or "civil rights" in val:
            return "Equity Mandate"
        elif "tribe" in val or "nonprofit" in val:
            return "Community Inclusion"
        elif "shelter" in val or "evacuation" in val:
            return "Emergency Services"
        elif "federal standard" in val:
            return "Federal Standard"
        else:
            return "Other"

    if "Vulnerable Populations Protections" in filtered_df.columns:
        filtered_df["Protection Category"] = filtered_df["Vulnerable Populations Protections"].apply(simplify_protection)
        protection_summary = filtered_df["Protection Category"].value_counts().reset_index()
        protection_summary.columns = ["Category", "Count"]
        st.subheader("🛡️ Protection Categories")
        fig_protect = px.bar(protection_summary, x="Category", y="Count", title="Protection Categories")
        st.plotly_chart(fig_protect, use_container_width=True)

    if "Equity Initiatives" in filtered_df.columns:
        equity_counts = filtered_df["Equity Initiatives"].value_counts().reset_index()
        equity_counts.columns = ["Response", "Count"]
        fig_equity = px.pie(equity_counts, names="Response", values="Count", title="Equity Initiatives")
        st.plotly_chart(fig_equity, use_container_width=True)

    if "Mitigation Planning" in filtered_df.columns:
        mitigation_counts = filtered_df["Mitigation Planning"].value_counts().reset_index()
        mitigation_counts.columns = ["Response", "Count"]
        fig_mitigation = px.pie(mitigation_counts, names="Response", values="Count", title="Mitigation Planning")
        st.plotly_chart(fig_mitigation, use_container_width=True)
