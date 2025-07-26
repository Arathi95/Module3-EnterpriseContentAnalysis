import streamlit as st
from dotenv import load_dotenv
from src.content_analyzer import ContentAnalyzer

load_dotenv()

analyzer = ContentAnalyzer()

st.title("Enterprise Content Analysis Platform")

uploaded_file = st.file_uploader("Upload a business document", type=["txt", "md"])

if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8")
    st.text_area("Content", content, height=300)

    if st.button("Analyze Content"):
        with st.spinner("Analyzing..."):
            analysis = analyzer.analyze_content(content)
            st.subheader("Analysis")
            if "error" in analysis:
                st.error(analysis["error"])
            else:
                st.write(f"**Sentiment:** {analysis.get('sentiment', 'N/A')}")
                st.subheader("Summary")
                st.write(analysis.get('summary', 'No summary provided.'))
                st.subheader("Key Points")
                for point in analysis.get('key_points', []):
                    st.write(f"- {point}")
