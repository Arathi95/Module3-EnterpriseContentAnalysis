import os
import json
from openai import OpenAI

class ContentAnalyzer:
    """
    A class to analyze content using the OpenAI API.
    """
    def __init__(self):
        """
        Initializes the ContentAnalyzer and the OpenAI client.
        """
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def analyze_content(self, text: str) -> dict:
        """
        Analyzes the given text using GPT-4o-mini and returns a structured analysis.

        Args:
            text: The content to analyze.

        Returns:
            A dictionary containing the summary, sentiment, and key points.
        """
        prompt = f"""Analyze the following document and return a JSON object with the following structure:
{{
  "summary": "A concise summary of the document.",
  "sentiment": "positive, neutral, or negative",
  "key_points": [
    "Key point 1",
    "Key point 2",
    "Key point 3"
  ]
}}

Document:
{text}
"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                response_format={ "type": "json_object" },
                messages=[
                    {"role": "system", "content": "You are an expert content analyst. Provide the analysis in a JSON format."},
                    {"role": "user", "content": prompt}
                ]
            )
            analysis = json.loads(response.choices[0].message.content)
            return analysis
        except Exception as e:
            return {"error": f"An error occurred: {e}"}