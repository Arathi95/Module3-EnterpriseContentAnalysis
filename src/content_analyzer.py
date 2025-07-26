from openai import OpenAI
import os

def analyze_content(content: str) -> str:
    """
    Analyzes the given content using the OpenAI API.
    """
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=f"Analyze the following business document and provide a summary:\n\n{content}",
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"An error occurred: {e}"

