import streamlit as st
from dotenv import load_dotenv
from src.content_analyzer import ContentAnalyzer, ANALYSIS_TEMPLATES
from src.document_processor import DocumentProcessor
from src.cost_tracker import CostTracker
import os

load_dotenv()

analyzer = ContentAnalyzer()
cost_tracker = CostTracker()

st.set_page_config(layout="wide")

st.sidebar.title("Budget Tracker")
daily_usage = cost_tracker.get_daily_usage()
monthly_usage = cost_tracker.get_monthly_usage()
st.sidebar.metric(label="Daily Cost", value=f"${daily_usage['cost']:.2f}", delta=f"${cost_tracker.daily_limit - daily_usage['cost']:.2f} remaining")
st.sidebar.metric(label="Monthly Cost", value=f"${monthly_usage['cost']:.2f}", delta=f"${cost_tracker.monthly_limit - monthly_usage['cost']:.2f} remaining")


st.title("Enterprise Content Analysis Platform")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Upload Content for Analysis")
    analysis_type = st.selectbox(
        "Select Analysis Type",
        list(ANALYSIS_TEMPLATES.keys())
    )
    uploaded_file = st.file_uploader("Drag and drop your file here", type=['txt', 'md', 'pdf', 'docx'])
    
    content_input = None
    if uploaded_file is not None:
        try:
            # Save the uploaded file temporarily
            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Check supported file types before processing
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext not in [".pdf", ".docx", ".txt"]:
                st.error(f"Unsupported file type: {ext}. Please upload a PDF, DOCX, or TXT file.")
                os.remove(uploaded_file.name)
                content_input = None
            else:
                processor = DocumentProcessor(uploaded_file.name)
                processed_data = processor.process()
                content_input = processed_data["text"]
                metadata = processed_data["metadata"]

                st.info(f"File Type: {metadata['file_type']} | File Size: {metadata['file_size']} bytes | Token Count: {metadata['token_count']}")

                # Estimate cost
                input_tokens = metadata['token_count']
                output_tokens = 2048  # A reasonable estimate for the output
                estimated_cost = (input_tokens / 1_000_000) * cost_tracker.input_cost_per_million + \
                                 (output_tokens / 1_000_000) * cost_tracker.output_cost_per_million
                st.warning(f"Estimated cost for this analysis: ${estimated_cost:.4f}")

                os.remove(uploaded_file.name)

        except Exception as e:
            st.error(f"Error processing file: {e}")
            content_input = None

    analyze_button = st.button("Analyze Content")

with col2:
    st.subheader("Analysis Results")
    if analyze_button and uploaded_file is not None and content_input is not None:
        can_afford, reason = cost_tracker.can_afford_analysis(input_tokens, output_tokens)

        if not can_afford:
            st.error(f"Analysis cannot proceed: {reason}")
        else:
            with st.spinner("Analyzing..."):
                analysis = analyzer.analyze_content(content_input, analysis_type)
                
                # Record actual usage
                if "usage" in analysis:
                    cost_tracker.record_usage(analysis['usage']['prompt_tokens'], analysis['usage']['completion_tokens'])
                
                st.markdown("---")
                
                if "error" in analysis:
                    st.error(analysis["error"])
                else:
                    if analysis_type == "General Business":
                        st.subheader("Executive Summary")
                        st.info(analysis.get("executive_summary", "Not available."))

                        st.subheader("Content Classification")
                        classification = analysis.get("content_classification", {})
                        st.write(f"**Type:** {classification.get('content_type', 'N/A')}")
                        st.write(f"**Industry:** {classification.get('industry', 'N/A')}")
                        st.write(f"**Quality Score:** {classification.get('content_quality_score', 'N/A')}")

                        st.subheader("Sentiment Analysis")
                        sentiment = analysis.get("sentiment_analysis", {})
                        st.write(f"**Overall Sentiment:** {sentiment.get('overall_sentiment', 'N/A')}")
                        st.write(f"**Sentiment Score:** {sentiment.get('sentiment_score', 'N/A')}")
                        st.write(f"**Confidence:** {sentiment.get('confidence_score', 'N/A')}")

                        st.subheader("Key Insights")
                        for insight in analysis.get("key_insights", []):
                            st.success(f"**Finding:** {insight.get('finding', 'N/A')} | **Impact:** {insight.get('impact', 'N/A')}")

                        st.subheader("Strategic Implications")
                        implications = analysis.get("strategic_implications", {})
                        st.write("**Opportunities:**")
                        for opp in implications.get("opportunities", []):
                            st.write(f"- {opp}")
                        st.write("**Risks:**")
                        for risk in implications.get("risks", []):
                            st.write(f"- {risk}")

                        st.subheader("Recommended Actions")
                        for action in analysis.get("recommended_actions", []):
                            st.warning(f"**Action:** {action.get('action_item', 'N/A')} | **Priority:** {action.get('priority', 'N/A')} | **Team:** {action.get('responsible_team', 'N/A')}")

                    elif analysis_type == "Competitive Intelligence":
                        st.subheader("Executive Summary")
                        st.info(analysis.get("executive_summary", "Not available."))

                        st.subheader("Competitor Profile")
                        profile = analysis.get("competitor_profile", {})
                        st.write(f"**Company:** {profile.get('company_name', 'N/A')}")
                        st.write(f"**Market Position:** {profile.get('market_position', 'N/A')}")
                        st.write("**Strengths:**")
                        for strength in profile.get("key_strengths", []):
                            st.write(f"- {strength}")
                        st.write("**Weaknesses:**")
                        for weakness in profile.get("key_weaknesses", []):
                            st.write(f"- {weakness}")

                        st.subheader("Strategic Analysis")
                        strategic = analysis.get("strategic_analysis", {})
                        st.write("**Competitive Threats:**")
                        for threat in strategic.get("competitive_threats", []):
                            st.error(f"- {threat.get('threat_description', 'N/A')} (Level: {threat.get('threat_level', 'N/A')})")
                        st.write("**Market Opportunities:**")
                        for opp in strategic.get("market_opportunities", []):
                            st.success(f"- {opp}")
                        st.write("**Strategic Recommendations:**")
                        for rec in strategic.get("strategic_recommendations", []):
                            st.warning(f"- {rec}")

                    elif analysis_type == "Customer Feedback":
                        st.subheader("Executive Summary")
                        st.info(analysis.get("executive_summary", "Not available."))

                        st.subheader("Feedback Classification")
                        classification = analysis.get("feedback_classification", {})
                        st.write(f"**Product/Service:** {classification.get('product_service', 'N/A')}")
                        st.write(f"**Feedback Type:** {classification.get('feedback_type', 'N/A')}")

                        st.subheader("Sentiment Analysis")
                        sentiment = analysis.get("sentiment_analysis", {})
                        st.write(f"**Overall Customer Satisfaction:** {sentiment.get('overall_customer_satisfaction', 'N/A')}")
                        st.write(f"**Satisfaction Score:** {sentiment.get('satisfaction_score', 'N/A')}")

                        st.subheader("Key Themes")
                        themes = analysis.get("key_themes", {})
                        st.write("**Top Pain Points:**")
                        for point in themes.get("top_pain_points", []):
                            st.error(f"- {point.get('pain_point', 'N/A')} (Frequency: {point.get('frequency', 'N/A')})")
                        st.write("**Top Praise Points:**")
                        for point in themes.get("top_praise_points", []):
                            st.success(f"- {point.get('praise_point', 'N/A')} (Frequency: {point.get('frequency', 'N/A')})")

                        st.subheader("Actionable Insights")
                        for insight in analysis.get("actionable_insights", []):
                            st.warning(f"**Recommendation:** {insight.get('recommendation', 'N/A')} | **Priority:** {insight.get('priority', 'N/A')} | **Impact:** {insight.get('impact_on_satisfaction', 'N/A')}")

                    with st.expander("View Raw JSON Analysis"):
                        st.json(analysis)
    elif analyze_button:
        st.warning("Please upload a file to analyze.")