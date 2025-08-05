import pandas as pd
import streamlit as st
import plotly.express as px

# Load dataset
df = pd.read_csv("Final_Combined_Emergency_Law_Data.csv")

# Sidebar filter
st.sidebar.header("Filter by State")
states = ["All States"] + sorted(df["State"].dropna().unique().tolist())
selected_state = st.sidebar.selectbox("Select a State", states)

# Filter data
if selected_state == "All States":
    filtered_df = df.copy()
else:
    filtered_df = df[df["State"] == selected_state]

title_state = selected_state if selected_state != "All States" else "All U.S. States"

# Tabs
tab1, tab2, tab3 = st.tabs([
    "METRICS", 
    "STATE CHARTS", 
    "PROTECTIONS"
])

# --- Tab 1: METRICS ---
with tab1:
    st.header(f"📊 Disaster Law Metrics – {title_state}")
    st.markdown("Key legislative and emergency preparedness markers for the selected region.")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🟡 Equity Initiatives")
        st.metric(label="", value=filtered_df["Equity Initiatives"].notna().sum())
    with col2:
        st.markdown("### 🔷 Mutual Aid Agreements")
        st.metric(label="", value=filtered_df["Mutual Aid"].str.lower().eq("yes").sum())
    with col3:
        st.markdown("### 🟢 Mitigation Planning")
        st.metric(label="", value=filtered_df["Mitigation Planning"].str.lower().eq("yes").sum())

    col4, col5 = st.columns(2)
    with col4:
        st.markdown("### 🧭 Emergency Powers (Local)")
        st.metric(label="", value=filtered_df["Local Emergency Powers"].str.lower().eq("yes").sum())
    with col5:
        st.markdown("### 🧒 Vulnerable Population Protection")
        st.metric(label="", value=filtered_df["Vulnerable Populations Protections"].notna().sum())

# --- Tab 2: STATE CHARTS ---
with tab2:
    st.header(f"📍 State-Level Breakdown – {title_state}")
    st.markdown("Visual summaries of record counts and authority indicators.")
    st.markdown("---")

    st.subheader("Entries by State")
    state_counts = filtered_df["State"].value_counts()
    if not state_counts.empty:
        st.bar_chart(state_counts)
    else:
        st.info("No entries found for this state.")

    st.subheader("Local Authority Enabled")
    local_authority_counts = filtered_df["Local Authority"].fillna("No").value_counts()
    if not local_authority_counts.empty:
        fig = px.pie(
            names=local_authority_counts.index, 
            values=local_authority_counts.values, 
            title="Local Authority Presence",
            hole=0.4
        )
        st.plotly_chart(fig)
    else:
        st.info("No local authority data available.")

# --- Tab 3: PROTECTIONS ---
with tab3:
    st.header(f"🛡️ Protections Overview – {title_state}")
    st.markdown("Focus on laws and measures protecting vulnerable populations.")
    st.markdown("---")

    protection_counts = filtered_df["Vulnerable Populations Protections"].dropna().value_counts()
    if not protection_counts.empty:
        fig2 = px.bar(
            x=protection_counts.index,
            y=protection_counts.values,
            labels={"x": "Protection", "y": "Count"},
            title="Types of Protections Across States"
        )
        fig2.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig2)
    else:
        st.info("No protection data available for this state.")

    # Equity Initiatives
    equity_df = filtered_df[filtered_df["Equity Initiatives"].notna()][["State", "Equity Initiatives"]].copy()

    def clean_initiative(text):
        if isinstance(text, str):
            if "http" in text:
                return f"[Learn more]({text})"
            return text.strip()
        return "Other"

    equity_df["Equity Label"] = equity_df["Equity Initiatives"].apply(clean_initiative)
    initiative_group = equity_df.groupby("Equity Label")["State"].apply(list).reset_index()
    initiative_group["Count"] = initiative_group["State"].apply(len)

    if not initiative_group.empty:
        st.subheader("📘 Equity Initiatives by Type")
        fig3 = px.pie(
            initiative_group,
            names="Equity Label",
            values="Count",
            title="Equity Initiative Types",
            hole=0.3
        )
        st.plotly_chart(fig3)

        st.markdown("### 📍 States by Equity Initiative")
        for _, row in initiative_group.iterrows():
            label = row["Equity Label"]
            states = ", ".join(sorted(row["State"]))
            with st.expander(label, expanded=False):
                st.write(states)
    else:
        st.info("No equity initiatives data available for this state.")
