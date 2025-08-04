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

ax_bar.set_xlabel('States', color='#2c3e50', fontsize=12, fontweight='bold')
ax_bar.set_ylabel('Number of Laws', color='#2c3e50', fontsize=12, fontweight='bold')
ax_bar.set_xticks(range(len(state_count)))
ax_bar.set_xticklabels(state_count.index, rotation=45, ha='right', color='#2c3e50')
ax_bar.tick_params(colors='#2c3e50')
ax_bar.set_facecolor('white')
fig_bar.patch.set_facecolor('white')
ax_bar.grid(True, alpha=0.3, color='#dee2e6')

# Add value labels on bars
for i, v in enumerate(state_count.values):
    ax_bar.text(i, v + 0.1, str(v), ha='center', va='bottom', color='#2c3e50', fontweight='bold')

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
                                      textprops={'color': '#2c3e50', 'fontsize': 12, 'fontweight': 'bold'})

# Customize the percentage text
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(14)

ax_pie.axis("equal")
fig_pie.patch.set_facecolor('white')
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
        /* Page background - clean white/grey */
        .stApp {
            background-color: #f8f9fa;
        }
        
        /* Text colors - dark for readability on light background */
        h1, h2, h3, h4, h5, h6, p, div, span {
            color: #2c3e50 !important;
        }
        
        /* Sidebar styling - light grey */
        section[data-testid="stSidebar"] {
            background-color: #e9ecef;
        }
        
        /* Sidebar text */
        .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar h4, .stSidebar h5, .stSidebar h6, .stSidebar p, .stSidebar div, .stSidebar span, .stSidebar label {
            color: #2c3e50 !important;
        }
        
        /* Metric styling - subtle background with green accent */
        [data-testid="metric-container"] {
            background-color: white;
            border: 2px solid #2d584a;
            padding: 1rem;
            border-radius: 0.5rem;
            box-shadow: 0 2px 4px rgba(45, 88, 74, 0.1);
        }
        
        /* DataFrame styling */
        .stDataFrame {
            background-color: white;
            border-radius: 0.5rem;
        }
        
        /* Download button styling */
        .stDownloadButton > button {
            background-color: #2d584a;
            color: white;
            border: none;
            border-radius: 0.5rem;
            padding: 0.5rem 1rem;
            font-weight: bold;
        }
        
        .stDownloadButton > button:hover {
            background-color: #1f4032;
            color: white;
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(45, 88, 74, 0.3);
        }
        
        /* Warning message styling */
        .stAlert {
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
        }
    </style>
    """,
    unsafe_allow_html=True
)
