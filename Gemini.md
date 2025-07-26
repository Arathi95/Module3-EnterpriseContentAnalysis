# Enterprise Content Analysis Platform

This file tracks the setup and execution for the Enterprise Content Analysis Platform.

## Project Structure

- `app.py`: The main Streamlit application.
- `src/content_analyzer.py`: Contains the `ContentAnalyzer` class for interacting with the OpenAI API.
- `src/document_processor.py`: Handles file processing for various formats.
- `requirements.txt`: Project dependencies.
- `.env.example`: Example environment file for API keys.
- `Gemini.md`: This file.

## Features

- **Professional Title**: The application has a professional title "Enterprise Content Analysis Platform".
- **File Upload for Content**: A file uploader allows users to drag and drop files (TXT, MD, PDF, DOCX) for analysis, replacing the manual text input.
- **Advanced Document Processing**:
  - Handles PDF, DOCX, and TXT file formats.
  - Extracts and cleans text from documents.
  - Optimizes content length to a maximum of 3000 tokens using `tiktoken` to manage API costs.
  - Provides document metadata, including file type, size, and token count.
- **Analyze Button**: An "Analyze" button initiates the content analysis process.
- **Formatted Results**: The analysis results are displayed in a clean and organized format.
- **Cost Estimation**: The application shows an estimated cost of $0.05 for each analysis.
- **Layout**: The application uses a two-column layout for a better user experience.
- **Advanced Prompt Engineering**:
  - **Persona-Driven Analysis**: Utilizes a senior business analyst persona (SYSTEM_PROMPT) for high-quality, insightful analysis.
  - **Structured JSON Output**: Returns a detailed JSON object with a predefined ANALYSIS_TEMPLATE.
  - **Consistent Output**: The temperature is set to 0.3 to ensure consistent analysis results.
- **Multi-Type Analysis**:
  - **Analysis Type Selection**: A dropdown menu allows users to select from different analysis types (General Business, Competitive Intelligence, Customer Feedback).
  - **Custom Prompt Templates**: Each analysis type uses a specialized prompt template to guide the AI for targeted insights.
  - **Dynamic Output Rendering**: The application dynamically adjusts to display the structured results for the selected analysis type.

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
