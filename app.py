import streamlit as st
from dotenv import load_dotenv
import os
from src.content_analyzer import analyze_content

load_dotenv()

st.title("Enterprise Content Analysis Platform")

uploaded_file = st.file_uploader("Upload a business document", type=["txt", "md"])

if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8")
    st.text_area("Content", content, height=300)

    if st.button("Analyze Content"):
        with st.spinner("Analyzing..."):
            analysis = analyze_content(content)
            st.subheader("Analysis")
            st.write(analysis)
