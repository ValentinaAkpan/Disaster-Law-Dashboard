import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(page_title="Disaster Law Dashboard", layout="wide")
st.title("Disaster Law Dashboard for US States")

# Load data
DATA_PATH = "Final_Combined_Emergency_Law_Data.csv"

@st.cache_data
def load_data(path):
    return pd.read_csv(path)

df = load_data(DATA_PATH)
df.columns = [col.strip() for col in df.columns]

# Top filter
st.markdown("### Filter by State")
all_states = sorted(df["State"].dropna().unique())
state_options = ["All States"] + all_states
selected_state = st.selectbox("Select a State", state_options, index=0)

# Filter logic
filtered_df = df if selected_state == "All States" else df[df["State"] == selected_state]

# Custom tab styling
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab"] {
        font-weight: bold !important;
        font-size: 22px !important;
        padding: 1rem 2rem !important;
        margin-right: 2rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# Define tabs
tab1, tab2, tab3 = st.tabs(["Metrics", "State Charts", "Protections"])

# Function to get count and states for "yes" responses
def get_yes_states(column):
    if column not in filtered_df.columns:
        return "No data", []
    df_yes = filtered_df[filtered_df[column].str.lower() == "yes"]
    count = len(df_yes)
    states = df_yes["State"].dropna().unique().tolist()
    return count, states

# Metrics Tab
with tab1:
    metrics = {
        "Equity Initiatives": "Equity Initiatives",
        "Mutual Aid Agreements": "Mutual Aid",
        "Mitigation Planning": "Mitigation Planning",
        "Emergency Powers (Local)": "Local Emergency Powers"
    }

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    for col, (label, field) in zip([col1, col2, col3, col4], metrics.items()):
        count, states = get_yes_states(field)
        with col:
            st.metric(label, count)
            if states:
                st.caption(", ".join(sorted(states)))
            else:
                st.caption("No states with this status")

# State Charts Tab
with tab2:
    st.subheader("Number of Entries per State")

    if filtered_df.empty:
        st.warning("No data available for the selected state.")
    else:
        if "State" in filtered_df.columns:
            state_count = filtered_df["State"].value_counts().reset_index()
            state_count.columns = ["State", "Count"]
            fig_bar = px.bar(state_count, x="State", y="Count", title="Entries per State")
            st.plotly_chart(fig_bar, use_container_width=True)

        if "Local Authority" in filtered_df.columns:
            st.subheader("Local Authority Enabled")
            authority_count = filtered_df["Local Authority"].value_counts().reset_index()
            authority_count.columns = ["Response", "Count"]
            fig_pie = px.pie(authority_count, names="Response", values="Count", title="Local Authority Status")
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No data on Local Authority.")

# Protections Tab
with tab3:
    if filtered_df.empty:
        st.warning("No data available for the selected state.")
    else:
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
            st.subheader("Protection Categories")
            fig_protect = px.bar(protection_summary, x="Category", y="Count", title="Protection Categories")
            st.plotly_chart(fig_protect, use_container_width=True)
        else:
            st.info("No data on Vulnerable Populations Protections.")

        if "Equity Initiatives" in filtered_df.columns:
            equity_counts = filtered_df["Equity Initiatives"].value_counts().reset_index()
            equity_counts.columns = ["Response", "Count"]
            fig_equity = px.pie(equity_counts, names="Response", values="Count", title="Equity Initiatives")
            st.plotly_chart(fig_equity, use_container_width=True)
        else:
            st.info("No data on Equity Initiatives.")

        if "Mitigation Planning" in filtered_df.columns:
            mitigation_counts = filtered_df["Mitigation Planning"].value_counts().reset_index()
            mitigation_counts.columns = ["Response", "Count"]
            fig_mitigation = px.pie(mitigation_counts, names="Response", values="Count", title="Mitigation Planning")
            st.plotly_chart(fig_mitigation, use_container_width=True)
        else:
            st.info("No data on Mitigation Planning.")
