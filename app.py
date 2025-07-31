import streamlit as st
from dotenv import load_dotenv
from src.content_analyzer import ContentAnalyzer, ANALYSIS_TEMPLATES
from src.document_processor import DocumentProcessor
from src.cost_tracker import CostTracker
import plotly.express as px
import pandas as pd
import os

load_dotenv()

analyzer = ContentAnalyzer()
cost_tracker = CostTracker()


st.set_page_config(layout="wide")

# --- Analytics Dashboard Tabs ---
tab1, tab2, tab3 = st.tabs(["Single Analysis", "Batch Processing", "Analytics"])
# --- ANALYTICS TAB ---
###############################
with tab3:
    st.title("Interactive Analytics Dashboard")
    st.write("Visualize key metrics from your analyses.")

    # Placeholder: Load or simulate batch results DataFrame
    # In production, replace this with actual batch results from previous analyses
    # Example columns: Document, Type, Sentiment, Business Impact, Confidence, Cost
    if os.path.exists("batch_results.csv"):
        df = pd.read_csv("batch_results.csv")
    else:
        # Simulated data for demo purposes (all arrays must be length 20)
        df = pd.DataFrame({
            "Document": [f"Doc {i+1}" for i in range(20)],
            "Type": (["General Business", "Competitive Intelligence", "Customer Feedback"] * 7)[:20],
            "Sentiment": (["Positive", "Negative", "Neutral", "Mixed"] * 5)[:20],
            "Business Impact": (["High", "Medium", "Low"] * 7)[:20],
            "Confidence": [round(abs(0.7 + 0.2 * ((i % 5) - 2)), 2) for i in range(20)],
            "Cost": [round(0.05 + 0.01 * (i % 7), 2) for i in range(20)]
        })

    colA, colB = st.columns(2)
    with colA:
        st.subheader("Sentiment Distribution")
        fig_sentiment = px.pie(df, names="Sentiment", title="Sentiment Distribution")
        st.plotly_chart(fig_sentiment, use_container_width=True)

        st.subheader("Business Impact Breakdown")
        impact_counts = df["Business Impact"].value_counts().reset_index()
        impact_counts.columns = ["Business Impact", "Count"]
        fig_impact = px.bar(impact_counts, x="Business Impact", y="Count", title="Business Impact Bar Chart")
        st.plotly_chart(fig_impact, use_container_width=True)

    with colB:
        st.subheader("Confidence Score Histogram")
        fig_conf = px.histogram(df, x="Confidence", nbins=10, title="Confidence Score Distribution")
        st.plotly_chart(fig_conf, use_container_width=True)

        st.subheader("Cost per Document")
        fig_cost = px.bar(df, x="Document", y="Cost", title="Cost per Document", labels={"Cost": "$USD"})
        st.plotly_chart(fig_cost, use_container_width=True)

    st.subheader("Content Type Breakdown")
    fig_type = px.pie(df, names="Type", title="Content Type Breakdown")
    st.plotly_chart(fig_type, use_container_width=True)

# --- SINGLE ANALYSIS TAB ---
with tab1:
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
        uploaded_file = st.file_uploader("Drag and drop your file here", type=['txt', 'md', 'pdf', 'docx'], key="single_upload")
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

        analyze_button = st.button("Analyze Content", key="single_analyze")

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

# --- BATCH PROCESSING TAB ---
import pandas as pd
from io import StringIO

with tab2:
    st.header("Batch Document Analysis")
    batch_analysis_type = st.selectbox(
        "Select Analysis Type (Batch)",
        list(ANALYSIS_TEMPLATES.keys()),
        key="batch_analysis_type"
    )
    uploaded_files = st.file_uploader(
        "Upload multiple files (TXT, PDF, DOCX)",
        type=["txt", "pdf", "docx"],
        accept_multiple_files=True,
        key="batch_upload"
    )
    batch_button = st.button("Run Batch Analysis")

    if batch_button and uploaded_files:
        docs = []
        file_names = []
        for idx, file in enumerate(uploaded_files):
            try:
                with open(file.name, "wb") as f:
                    f.write(file.getbuffer())
                ext = os.path.splitext(file.name)[1].lower()
                if ext not in [".pdf", ".docx", ".txt"]:
                    st.error(f"Unsupported file type: {ext} in {file.name}. Skipping.")
                    os.remove(file.name)
                    continue
                processor = DocumentProcessor(file.name)
                processed = processor.process()
                docs.append({
                    "id": file.name,
                    "text": processed["text"]
                })
                file_names.append(file.name)
                os.remove(file.name)
            except Exception as e:
                st.error(f"Error processing {file.name}: {e}")

        if docs:
            with st.spinner("Analyzing batch..."):
                results = analyzer.batch_analyze(docs, batch_analysis_type)
            # Prepare DataFrame
            rows = []
            for doc, result in zip(docs, results):
                res = result.get("result")
                error = result.get("error")
                usage = res.get("usage") if res else None
                cost = 0.0
                confidence = None
                sentiment = None
                impact = None
                doc_type = batch_analysis_type
                if res:
                    if batch_analysis_type == "General Business":
                        sentiment = res.get("sentiment_analysis", {}).get("overall_sentiment")
                        confidence = res.get("sentiment_analysis", {}).get("confidence_score")
                        impact = ", ".join([i.get("impact", "") for i in res.get("key_insights", []) if i.get("impact")])
                    elif batch_analysis_type == "Competitive Intelligence":
                        sentiment = None
                        confidence = None
                        impact = ", ".join([t.get("threat_level", "") for t in res.get("strategic_analysis", {}).get("competitive_threats", []) if t.get("threat_level")])
                    elif batch_analysis_type == "Customer Feedback":
                        sentiment = res.get("sentiment_analysis", {}).get("overall_customer_satisfaction")
                        confidence = res.get("sentiment_analysis", {}).get("satisfaction_score")
                        impact = ", ".join([i.get("impact_on_satisfaction", "") for i in res.get("actionable_insights", []) if i.get("impact_on_satisfaction")])
                    if usage:
                        cost = (usage['prompt_tokens'] / 1_000_000) * cost_tracker.input_cost_per_million + \
                               (usage['completion_tokens'] / 1_000_000) * cost_tracker.output_cost_per_million
                rows.append({
                    "Document": doc["id"],
                    "Type": doc_type,
                    "Sentiment": sentiment if sentiment is not None else (error or "N/A"),
                    "Business Impact": impact if impact else "N/A",
                    "Confidence": confidence if confidence is not None else "N/A",
                    "Cost": f"${cost:.4f}" if cost else "N/A"
                })
            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True)
            # Download CSV
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download Results as CSV",
                data=csv,
                file_name="batch_analysis_results.csv",
                mime="text/csv"
            )
            # Show total cost and average confidence
            total_cost = sum(float(r["Cost"].replace("$", "")) for r in rows if r["Cost"] != "N/A")
            confidences = [float(r["Confidence"]) for r in rows if r["Confidence"] != "N/A"]
            avg_conf = sum(confidences) / len(confidences) if confidences else 0.0
            st.info(f"Total Cost: ${total_cost:.4f}")
            st.info(f"Average Confidence: {avg_conf:.3f}")
        else:
            st.warning("No valid files to process.")


