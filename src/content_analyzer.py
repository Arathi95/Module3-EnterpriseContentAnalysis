import os
import json
from openai import OpenAI

SYSTEM_PROMPT = (
    "You are a senior business analyst with 20 years of experience in enterprise "
    "strategy and digital transformation. Your analysis is sharp, insightful, and "
    "trusted by C-suite executives. You communicate with clarity and precision, "
    "focusing on actionable outcomes. Your final output must be a JSON object."
)

ANALYSIS_TEMPLATES = {
    "General Business": {
        "executive_summary": "A concise, high-level summary of the key findings and strategic recommendations for a C-suite audience.",
        "content_classification": {
            "content_type": "e.g., Financial Report, Customer Feedback, Market Analysis, News Article, Legal Document",
            "industry": "e.g., Technology, Finance, Healthcare, Retail, Automotive",
            "content_quality_score": "A score from 0.0 to 1.0 assessing the clarity, coherence, and credibility of the content."
        },
        "sentiment_analysis": {
            "overall_sentiment": "Positive, Negative, Neutral, or Mixed",
            "sentiment_score": "A score from -1.0 (very negative) to 1.0 (very positive).",
            "confidence_score": "A score from 0.0 to 1.0 indicating the confidence in the sentiment analysis."
        },
        "key_insights": [
            {
                "finding": "A specific, data-driven observation from the content.",
                "impact": "High, Medium, or Low"
            }
        ],
        "strategic_implications": {
            "opportunities": [
                "Potential strategic opportunities identified from the analysis."
            ],
            "risks": [
                "Potential strategic risks or threats identified from the analysis."
            ]
        },
        "recommended_actions": [
            {
                "action_item": "A clear, concise, and actionable recommendation.",
                "priority": "Critical, High, Medium, Low",
                "responsible_team": "e.g., Marketing, Sales, Product, Engineering, Legal"
            }
        ]
    },
    "Competitive Intelligence": {
        "executive_summary": "A summary of the competitive landscape, highlighting key threats and opportunities.",
        "competitor_profile": {
            "company_name": "Name of the competitor being analyzed.",
            "market_position": "e.g., Leader, Challenger, Niche Player, New Entrant",
            "key_strengths": ["List of key strengths."],
            "key_weaknesses": ["List of key weaknesses."]
        },
        "strategic_analysis": {
            "competitive_threats": [
                {
                    "threat_description": "Description of a specific competitive threat.",
                    "threat_level": "High, Medium, or Low"
                }
            ],
            "market_opportunities": ["Description of potential market opportunities."],
            "strategic_recommendations": ["Actionable recommendations to improve competitive positioning."]
        }
    },
    "Customer Feedback": {
        "executive_summary": "A summary of customer sentiment, key satisfaction drivers, and top pain points.",
        "feedback_classification": {
            "product_service": "The specific product or service mentioned.",
            "feedback_type": "e.g., Bug Report, Feature Request, Usability Issue, General Praise"
        },
        "sentiment_analysis": {
            "overall_customer_satisfaction": "Positive, Negative, Neutral, or Mixed",
            "satisfaction_score": "A score from -1.0 (very dissatisfied) to 1.0 (very satisfied)."
        },
        "key_themes": {
            "top_pain_points": [
                {
                    "pain_point": "A specific issue or problem mentioned by customers.",
                    "frequency": "Number of times this pain point is mentioned."
                }
            ],
            "top_praise_points": [
                 {
                    "praise_point": "A specific positive aspect mentioned by customers.",
                    "frequency": "Number of times this praise point is mentioned."
                }
            ]
        },
        "actionable_insights": [
            {
                "recommendation": "A specific action to address customer feedback.",
                "priority": "High, Medium, or Low",
                "impact_on_satisfaction": "High, Medium, or Low"
            }
        ]
    }
}


class ContentAnalyzer:
    """
    A class to analyze content using the OpenAI API.
    """
    def __init__(self):
        """
        Initializes the ContentAnalyzer and the OpenAI client.
        """
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



    def analyze_content(self, text: str, analysis_type: str) -> dict:
        """
        Analyzes the given text using GPT-4o-mini and returns a structured analysis
        based on the selected analysis type.
        Args:
            text: The content to analyze.
            analysis_type: The type of analysis to perform.

        Returns:
            A dictionary containing the detailed business analysis.
        """
        if analysis_type not in ANALYSIS_TEMPLATES:
            return {"error": "Invalid analysis type selected."}

        template = ANALYSIS_TEMPLATES[analysis_type]

        prompt = (
            f"Please perform a '{analysis_type}' analysis on the following document. "
            f"Based on your expertise, populate the fields in this JSON structure:\n\n"
            f"{json.dumps(template, indent=2)}\n\n"
            f"Document to Analyze:\n"
            f"---------------------\n"
            f"{text}"
        )
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            analysis = json.loads(response.choices[0].message.content)
            analysis['usage'] = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens
            }
            return analysis
        except Exception as e:
            return {"error": f"An error occurred: {e}"}

    def batch_analyze(self, documents, analysis_type, progress_callback=None):
        """
        Processes a batch of documents with progress tracking, rate limiting, and error handling.

        Args:
            documents (list): List of dicts, each with at least 'id' and 'text' keys.
            analysis_type (str): The type of analysis to perform.
            progress_callback (callable, optional): Function accepting progress (0.0-1.0) for UI updates.

        Returns:
            list: List of dicts with 'id', 'timestamp', 'result', and 'error' (if any).
        """
        import time
        from datetime import datetime

        results = []
        total = len(documents)
        for idx, doc in enumerate(documents):
            doc_id = doc.get('id', idx)
            text = doc.get('text', '')
            timestamp = datetime.utcnow().isoformat()
            try:
                result = self.analyze_content(text, analysis_type)
                error = result.get('error')
            except Exception as e:
                result = None
                error = str(e)
            results.append({
                'id': doc_id,
                'timestamp': timestamp,
                'result': result if not error else None,
                'error': error
            })
            # Progress bar update
            if progress_callback:
                progress_callback((idx + 1) / total)
            # Rate limiting
            if idx < total - 1:
                time.sleep(0.5)
        return results