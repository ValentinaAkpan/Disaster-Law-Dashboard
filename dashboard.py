import streamlit as st 
import pandas as pd
import os
import matplotlib.pyplot as plt 

# Check if file exists
if not os.path.exists("Final_csv.csv"):
    st.error("The data file 'Final_csv.csv' was not found.")
    st.stop()

# Load data
df = pd.read_csv("Final_csv.csv")

# App title
st.title("Disaster Law Dashboard for US States")

# Basic Metrics
st.subheader("Basic Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Unique States", df["State"].nunique())

with col2:
    st.metric("Local Authority Enabled", df['Local Authority'].str.lower().eq("yes").sum())

with col3:
    st.metric("Has Vulnerable Population Protection", df["Vulnerable Populations Protections"].notna().sum())

# Laws per state
state_count = df["State"].value_counts()
st.subheader("Number of Laws per State")
st.bar_chart(state_count)

# Local authority pie chart
authority_count = df["Local Authority"].value_counts()
st.subheader("Local Authority Enabled (Yes/No)")

st.write(authority_count)

fig, ax = plt.subplots(figsize=(5, 5))
ax.pie(authority_count, labels=authority_count.index, autopct="%1.1f%%", startangle=90)
ax.axis("equal")
st.pyplot(fig)

# Sidebar filter
st.sidebar.subheader("Filter by State")

selected_state = st.sidebar.selectbox("Select State", sorted(df["State"].unique()))

filtered_df = df[df["State"] == selected_state]

st.write(f"Showing data for **{selected_state}**")

if filtered_df.empty:
    st.warning("No data available for selected state.")
else:
    st.dataframe(filtered_df)

    # Download button
    st.download_button(
        label="Download Filtered Data as CSV",  
        data=filtered_df.to_csv(index=False),
        file_name=f"{selected_state}_laws.csv",
        mime='text/csv'
    )

# Custom CSS styling
st.markdown(
    """
    <style>
        .stApp {
            background-color: #2d584a;
        }
        h1, h2, h3, h4, h5, h6, p, div {
            color: white;
        }
        section[data-testid="stSidebar"] {
            background-color: #1f4032;
        }
    </style>
    """,
    unsafe_allow_html=True
)
