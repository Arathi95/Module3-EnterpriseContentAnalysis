# Enterprise Content Analysis Platform

This file tracks the setup and execution for the Enterprise Content Analysis Platform.

## Project Structure

- `app.py`: The main Streamlit application.
- `src/content_analyzer.py`: Contains the `ContentAnalyzer` class for interacting with the OpenAI API.
- `requirements.txt`: Project dependencies.
- `.env.example`: Example environment file for API keys.
- `Gemini.md`: This file.

## Features

- **Professional Title**: The application has a professional title "Enterprise Content Analysis Platform".
- **Content Input**: A text area is provided for users to paste the content they want to analyze.
- **Analyze Button**: An "Analyze" button initiates the content analysis process.
- **Formatted Results**: The analysis results are displayed in a clean and organized format.
- **Cost Estimation**: The application shows an estimated cost of $0.05 for each analysis.
- **Layout**: The application uses a two-column layout for a better user experience.

## Setup Instructions

### 1. Create Virtual Environment and Install Dependencies

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy the example .env file:

```bash
cp .env.example .env
```

Then, edit the `.env` file to add your OpenAI API key.

### 3. Run the Application

```bash
streamlit run app.py
```
