import streamlit as st
from dotenv import load_dotenv
from src.content_analyzer import ContentAnalyzer

load_dotenv()

analyzer = ContentAnalyzer()

st.set_page_config(layout="wide")

st.title("Enterprise Content Analysis Platform")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Enter Content to Analyze")
    content_input = st.text_area("Paste your content here", height=400)
    
    analyze_button = st.button("Analyze Content")

with col2:
    st.subheader("Analysis Results")
    if analyze_button:
        if content_input:
            with st.spinner("Analyzing..."):
                analysis = analyzer.analyze_content(content_input)
                
                st.markdown("---")
                
                if "error" in analysis:
                    st.error(analysis["error"])
                else:
                    st.write(f"**Sentiment:** {analysis.get('sentiment', 'N/A')}")
                    
                    st.subheader("Summary")
                    st.info(analysis.get('summary', 'No summary provided.'))
                    
                    st.subheader("Key Points")
                    for point in analysis.get('key_points', []):
                        st.success(f"- {point}")

                    st.markdown("---")
                    st.subheader("API Cost Estimate")
                    st.warning("$0.05")
        else:
            st.warning("Please paste some content to analyze.")