import streamlit as st 
import pandas as pd
import os
import matplotlib.pyplot as plt 
import numpy as np

df = pd.read_csv("Final_csv.csv")

# Define custom color palette
primary_color = "#2d584a"
secondary_color = "#1f4032"
accent_color = "#4a7c59"  # Lighter green for variety
light_accent = "#6b9b7f"  # Even lighter for contrast

st.title("Disaster Law Dashboard for US States")
st.subheader("Basic Metrics")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Unique States", df["State"].nunique())
with col2:
    st.metric("Local Authority Enabled", df['Local Authority'].str.lower().eq("yes").sum())
with col3:
    st.metric("Has Vulnerable Population Protection", df["Vulnerable Populations Protections"].notna().sum())

# Bar chart with custom colors
state_count = df["State"].value_counts()
st.subheader("Number of Laws per State")

# Create a custom bar chart using matplotlib for better color control
fig_bar, ax_bar = plt.subplots(figsize=(12, 6))
bars = ax_bar.bar(range(len(state_count)), state_count.values, 
                  color=primary_color, edgecolor=secondary_color, linewidth=1.5)

# Add some variation with alternating colors
for i, bar in enumerate(bars):
    if i % 2 == 0:
        bar.set_color(primary_color)
    else:
        bar.set_color(accent_color)

ax_bar.set_xlabel('States', color='white', fontsize=12)
ax_bar.set_ylabel('Number of Laws', color='white', fontsize=12)
ax_bar.set_xticks(range(len(state_count)))
ax_bar.set_xticklabels(state_count.index, rotation=45, ha='right', color='white')
ax_bar.tick_params(colors='white')
ax_bar.set_facecolor('none')
fig_bar.patch.set_facecolor('none')

# Add value labels on bars
for i, v in enumerate(state_count.values):
    ax_bar.text(i, v + 0.1, str(v), ha='center', va='bottom', color='white', fontweight='bold')

st.pyplot(fig_bar)

# Local Authority Analysis
authority_count = df["Local Authority"].value_counts()
st.subheader("Local Authority Enabled (Yes/No)")
st.write(authority_count)

# Pie chart with custom colors
fig_pie, ax_pie = plt.subplots(figsize=(8, 8))
colors = [primary_color, secondary_color]  # Custom colors for pie slices

wedges, texts, autotexts = ax_pie.pie(authority_count.values, 
                                      labels=authority_count.index, 
                                      autopct="%1.1f%%", 
                                      startangle=90,
                                      colors=colors,
                                      textprops={'color': 'white', 'fontsize': 12, 'fontweight': 'bold'})

# Customize the percentage text
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(14)

ax_pie.axis("equal")
fig_pie.patch.set_facecolor('none')
st.pyplot(fig_pie)

# Sidebar filters
st.sidebar.subheader("Filter By State")
selected_state = st.sidebar.selectbox("Select State", df["State"].unique())
filtered_df = df[df["State"] == selected_state]

st.write(f"Showing Data For **{selected_state}**")
if filtered_df.empty:
    st.warning("No data available for selected state.")
else:
    st.dataframe(filtered_df)

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
        /* Page background */
        .stApp {
            background-color: #2d584a;
        }
        
        /* Text colors for contrast */
        h1, h2, h3, h4, h5, h6, p, div, span {
            color: white !important;
        }
        
        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: #1f4032;
        }
        
        /* Sidebar text */
        .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar h4, .stSidebar h5, .stSidebar h6, .stSidebar p, .stSidebar div, .stSidebar span, .stSidebar label {
            color: white !important;
        }
        
        /* Metric styling */
        [data-testid="metric-container"] {
            background-color: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 1rem;
            border-radius: 0.5rem;
        }
        
        /* DataFrame styling */
        .stDataFrame {
            background-color: rgba(255, 255, 255, 0.1);
        }
        
        /* Download button styling */
        .stDownloadButton > button {
            background-color: #4a7c59;
            color: white;
            border: none;
        }
        
        .stDownloadButton > button:hover {
            background-color: #6b9b7f;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)
