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

# Tabs
tab1, tab2, tab3 = st.tabs(["METRICS", "STATE CHARTS", "PROTECTIONS"])

# --- Tab 1: METRICS ---
with tab1:
    st.header("Disaster Law Metrics")
    # Collect metric values
    metrics = {
        "Equity Initiatives": filtered_df["Equity Initiatives"].notna().sum(),
        "Mutual Aid Agreements": filtered_df["Mutual Aid"].str.lower().eq("yes").sum(),
        "Mitigation Planning": filtered_df["Mitigation Planning"].str.lower().eq("yes").sum(),
        "Emergency Powers (Local)": filtered_df["Local Emergency Powers"].str.lower().eq("yes").sum(),
        "Vulnerable Population Protection": filtered_df["Vulnerable Populations Protections"].notna().sum()
    }
    # Inject styles for horizontal cards
    st.markdown("""
        <style>
        /* Ensure the app takes full width */
        .stApp {
            max-width: 1200px !important;
            margin: 0 auto;
        }
        .horizontal-cards {
            display: flex;
            flex-direction: row;
            flex-wrap: nowrap;
            gap: 16px;
            margin: 20px 0;
            justify-content: flex-start;
            align-items: stretch;
            width: 100%;
            min-width: 800px; /* Minimum width to enforce horizontal layout */
            overflow-x: auto; /* Allow horizontal scrolling if needed */
            box-sizing: border-box;
        }
        .metric-card {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            min-width: 150px; /* Reduced for better fit */
            max-width: 200px;
            flex: 1 1 150px;
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            transition: transform 0.2s ease;
        }
        .metric-card:hover {
            transform: translateY(-4px);
        }
        .metric-card h4 {
            font-size: 16px;
            margin: 0;
            color: #333;
            font-weight: 600;
        }
        .metric-card p {
            font-size: 28px;
            font-weight: bold;
            margin: 12px 0 0;
            color: #1a73e8;
        }
        /* Responsive adjustments */
        @media (max-width: 800px) {
            .horizontal-cards {
                flex-wrap: wrap;
                min-width: 0;
                justify-content: center;
            }
            .metric-card {
                min-width: 140px;
                max-width: 180px;
                padding: 15px;
            }
            .metric-card h4 {
                font-size: 14px;
            }
            .metric-card p {
                font-size: 24px;
            }
        }
        </style>
    """, unsafe_allow_html=True)
    # Render horizontal cards
    st.markdown('<div class="horizontal-cards">', unsafe_allow_html=True)
    for label, value in metrics.items():
        st.markdown(f"""
            <div class="metric-card">
                <h4>{label}</h4>
                <p>{value}</p>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Tab 2 and Tab 3 remain unchanged ---
# [Your existing code for Tab 2 and Tab 3 goes here, unchanged]
