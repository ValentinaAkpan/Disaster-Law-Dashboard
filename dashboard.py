import streamlit as st 
import pandas as pd
import os
import matplotlib.pyplot as plt 

df = pd.read_csv("Final_csv.csv")

st.title("Disaster Law Dashboard for US States")

st.subheader("Basic Matrics")

col1 , col2 , col3 = st.columns(3)

with col1:
    st.metric("Unique State",df["State"].nunique())

with col2:
    st.metric("Loacal Authority Enabled", df['Local Authority'].str.lower().eq("yes").sum())

with col3:
    st.metric("Has Vulnerable Population Protection",df["Vulnerable Populations Protections"].notna().sum())


state_count = df["State"].value_counts()

st.subheader("Number of Laws per state")

st.bar_chart(state_count)

authority_count = df["Local Authority"].value_counts()

st.subheader("Local Authoeity Enabled (Yes/No)")

st.write(authority_count)

fig , ax = plt.subplots()

ax.pie(authority_count,labels = authority_count.index , autopct = "%1.1f%%",startangle = 90)

ax.axis("equal")

st.pyplot(fig)

st.sidebar.subheader("Filter By state")

slected_state = st.sidebar.selectbox("Select State",df["State"].unique())

filtered_df = df[df["State"] == slected_state]

st.write(f"Show Data For **{slected_state}**")

if filtered_df.empty:
    st.warning("No data available for selected state.")
else:
    st.dataframe(filtered_df)

st.download_button(
    label="Download Filtered Data as CSV",  
    data=filtered_df.to_csv(index=False),
    file_name=f"{slected_state}_laws.csv",
    mime='text/csv'
)

st.markdown(
    """
    <style>
        /* Page background */
        .stApp {
            background-color: #2d584a;
        }

        /* Optional: Change text color for contrast */
        h1, h2, h3, h4, h5, h6, p, div {
            color: white;
        }

        /* Optional: Change sidebar background */
        section[data-testid="stSidebar"] {
            background-color: #1f4032;
        }
    </style>
    """,
    unsafe_allow_html=True
)
