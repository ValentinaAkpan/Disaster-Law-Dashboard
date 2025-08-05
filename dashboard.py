import pandas as pd
import streamlit as st
import plotly.express as px

# Load dataset
df = pd.read_csv("Final_Combined_Emergency_Law_Data.csv")

# Sidebar filter
st.sidebar.header("Filter by State")
states = ["All States"] + sorted(df["State"].dropna().unique().tolist())
selected_state = st.sidebar.selectbox("Select a State", states)

filtered_df = df.copy() if selected_state == "All States" else df[df["State"] == selected_state]

# Tab layout
tab1, tab2, tab3 = st.tabs(["**METRICS**", "**STATE CHARTS**", "**PROTECTIONS**"])

# ---- TAB 1 ----
with tab1:
    st.header("Disaster Law Metrics")

    metrics = {
        "Equity Initiatives": filtered_df["Equity Initiatives"].notna().sum(),
        "Mutual Aid Agreements": filtered_df["Mutual Aid"].str.lower().eq("yes").sum(),
        "Mitigation Planning": filtered_df["Mitigation Planning"].str.lower().eq("yes").sum(),
        "Emergency Powers (Local)": filtered_df["Local Emergency Powers"].str.lower().eq("yes").sum(),
        "Vulnerable Population Protection": filtered_df["Vulnerable Populations Protections"].notna().sum()
    }

    # Horizontal card layout
    st.markdown("""
        <style>
        .card-container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            margin-top: 20px;
        }
        .card {
            background-color: #fafafa;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 1px 6px rgba(0,0,0,0.05);
            width: 230px;
            min-height: 120px;
            text-align: left;
            flex: 1;
        }
        .card h4 {
            margin: 0;
            font-size: 16px;
            color: #333;
        }
        .card p {
            font-size: 32px;
            font-weight: bold;
            margin: 10px 0 0;
            color: #111;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    for label, value in metrics.items():
        st.markdown(f"""
            <div class="card">
                <h4>{label}</h4>
                <p>{value}</p>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---- TAB 2 ----
with tab2:
    st.header("State Charts")

    st.subheader("Number of Entries per State")
    state_counts = filtered_df["State"].value_counts()
    if not state_counts.empty:
        st.bar_chart(state_counts)
    else:
        st.warning("No data available for selected state.")

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
        st.warning("No Local Authority data available for selected state.")

# ---- TAB 3 ----
with tab3:
    st.header("Vulnerable Populations Protections")

    protection_counts = filtered_df["Vulnerable Populations Protections"].dropna().value_counts()
    if not protection_counts.empty:
        fig2 = px.bar(
            x=protection_counts.index,
            y=protection_counts.values,
            labels={"x": "Protection", "y": "Count"},
            title="Protections Across All States"
        )
        fig2.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig2)
    else:
        st.warning("No vulnerable population protections data available for this state.")

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
        st.subheader("Equity Initiatives by Type")
        fig3 = px.pie(
            initiative_group,
            names="Equity Label",
            values="Count",
            title="Equity Initiatives",
            hole=0.3
        )
        st.plotly_chart(fig3)

        st.markdown("### States by Equity Initiative")
        for _, row in initiative_group.iterrows():
            label = row["Equity Label"]
            states = ", ".join(sorted(row["State"]))
            with st.expander(label, expanded=False):
                st.write(states)
    else:
        st.warning("No equity initiatives data available for this state.")
