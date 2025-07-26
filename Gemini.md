# Enterprise Content Analysis Platform

This file tracks the setup and execution for the Enterprise Content Analysis Platform.

## Project Structure

- `app.py`: The main Streamlit application.
- `src/content_analyzer.py`: Contains the `ContentAnalyzer` class for interacting with the OpenAI API.
- `src/document_processor.py`: Handles file processing for various formats.
- `src/cost_tracker.py`: Tracks API usage and costs.
- `requirements.txt`: Project dependencies.
- `.env.example`: Example environment file for API keys.
- `Gemini.md`: This file.

# Gemini.md

## Streamlit App Features (as of July 2025)

### File Upload Support
- Users can upload PDF, DOCX, or TXT files for analysis.
- After upload, the app displays:
  - File type
  - File size (in bytes)
  - Token count (using tiktoken)
  - Estimated cost for analysis

### Document Processing
- Uploaded files are processed using the `DocumentProcessor` class.
- Only supported file types (.pdf, .docx, .txt) are accepted.
- If an unsupported file type is uploaded, a clear error message is shown to the user.

### Cost Tracking
- The sidebar displays:
  - Daily cost and remaining budget
  - Monthly cost and remaining budget
- Cost is estimated before analysis and tracked after analysis using `CostTracker`.

### Error Handling
- Errors during file processing (including unsupported file types) are caught and shown as user-friendly messages.

### Recommendations for Future Updates
- If new file types are supported, update both the UI and `DocumentProcessor`.
- Keep this file updated with any new user-facing features or error handling improvements.
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
