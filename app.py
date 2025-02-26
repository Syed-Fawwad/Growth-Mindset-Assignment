import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Streamlit App Configuration
st.set_page_config(page_title="Q3 Assignment 01 - Data Sweeper", page_icon="📊", layout="wide")

# Custom CSS for Professional UI
st.markdown(
    """
    <style>
        body {
            background: linear-gradient(to right, #ece9e6, #ffffff);
            font-family: 'Arial', sans-serif;
        }
        .title {
            font-size: 36px;
            font-weight: bold;
            color: #1a1a2e;
            text-align: center;
            margin-top: 20px;
        }
        .subtitle {
            font-size: 18px;
            color: #444;
            text-align: center;
            margin-bottom: 30px;
        }
        .card {
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .stButton>button {
            background: linear-gradient(135deg, #6a11cb, #2575fc);
            color: white;
            font-size: 18px;
            padding: 10px;
            border-radius: 8px;
            transition: 0.3s;
            border: none;
        }
        .stButton>button:hover {
            transform: scale(1.05);
            background: linear-gradient(135deg, #2575fc, #6a11cb);
        }
        .stFileUploader>div {
            border: 2px dashed #6a11cb;
            padding: 15px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# 🚀 Growth Mindset Introduction
st.markdown("<div class='title'>🚀 Growth Mindset Challenge</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>A growth mindset helps you embrace challenges, learn from failures, and continuously improve.</div>", unsafe_allow_html=True)

st.markdown(
    """
    ## 🌱 What is a Growth Mindset?  
    A growth mindset is the belief that intelligence, talents, and abilities can be developed through dedication, learning, and persistence.  
    People with a growth mindset embrace challenges, learn from failures, and continuously improve their skills.  

    ### 🔥 Why is a Growth Mindset Important?  
    Having a growth mindset can transform your life. It helps you:  
    ✅ Embrace challenges instead of avoiding them  
    ✅ Learn from criticism rather than feeling discouraged  
    ✅ Keep going despite failures instead of giving up  
    ✅ See effort as the key to success  
    ✅ Develop resilience and overcome difficulties  
    """,
    unsafe_allow_html=True
)

# 📂 Data Sweeper Section
st.markdown("<div class='title'>📂 Data Sweeper</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Transform your files between CSV and Excel formats with built-in data cleaning and visualization.</div>", unsafe_allow_html=True)

# File Upload Section
st.markdown("<div class='card'>", unsafe_allow_html=True)
uploaded_files = st.file_uploader("📤 Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)
st.markdown("</div>", unsafe_allow_html=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_ext = os.path.splitext(uploaded_file.name)[-1].lower()

        # Read File
        if file_ext == ".csv":
            df = pd.read_csv(uploaded_file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(uploaded_file)
        else:
            st.error("❌ Unsupported file format. Please upload a CSV or Excel file.")
            continue

        # Display File Info
        st.markdown(f"<div class='card'><h3>📄 {uploaded_file.name}</h3>", unsafe_allow_html=True)
        st.write(f"📏 File Size: {uploaded_file.size / 1024:.2f} KB")

        # Data Preview
        with st.expander("📌 *Preview Data*", expanded=True):
            st.dataframe(df.head())

        # Data Cleaning Options
        st.markdown("<h3>🛠 Data Cleaning</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            if st.button(f"🚀 Remove Duplicates from {uploaded_file.name}"):
                df.drop_duplicates(inplace=True)
                st.success("✅ Duplicates Removed!")

        with col2:
            if st.button(f"🔧 Fill Missing Values in {uploaded_file.name}"):
                numeric_cols = df.select_dtypes(include=["number"]).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.success("✅ Missing Values Filled!")

        # Select Columns to Keep
        with st.expander("🎯 *Select Columns to Keep*"):
            selected_columns = st.multiselect(f"Choose Columns for {uploaded_file.name}", df.columns, default=df.columns)
            df = df[selected_columns]

        # 📊 Data Visualization
        st.markdown("<h3>📊 Data Visualization</h3>", unsafe_allow_html=True)
        if st.checkbox(f"📈 Show Visualization for {uploaded_file.name}"):
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        # 🔄 Conversion Options
        st.markdown("<h3>🔄 File Conversion</h3>", unsafe_allow_html=True)
        conversion_type = st.radio(f"Convert {uploaded_file.name} to", ("CSV", "Excel"))

        if st.button(f"💾 Convert {uploaded_file.name} to {conversion_type}"):
            buffer = BytesIO()
            new_file_name = uploaded_file.name.replace(file_ext, f".{conversion_type.lower()}")

            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            st.download_button(
                label=f"⬇ Download {new_file_name}",
                data=buffer,
                file_name=new_file_name,
                mime=mime_type
            )

        st.markdown("</div>", unsafe_allow_html=True)  # Closing card

st.success("✅ All files processed successfully!")