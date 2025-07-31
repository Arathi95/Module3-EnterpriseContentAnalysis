# Analytics Dashboard Extension

## Overview
This project now includes an analytics dashboard in Streamlit with two tabs:
- **Single Analysis**: For analyzing a single document (existing functionality, now in a tab)
- **Batch Processing**: Upload multiple files, run batch analysis, and view results in a pandas DataFrame

## Batch Processing Features
- Supports multiple file uploads (TXT, PDF, DOCX)
- Results are shown in a DataFrame with columns:
  - Document, Type, Sentiment, Business Impact, Confidence, Cost
- Download results as CSV
- Displays total cost and average confidence for the batch

## Implementation Notes
- Uses `analyzer.batch_analyze` for batch processing
- Extracts relevant fields from each analysis type for DataFrame display
- Handles errors and unsupported file types gracefully
- Requires `pandas` for DataFrame and CSV export

## Future Improvements
- Add progress bar for batch analysis
- Support for more file types and larger files
- More granular error reporting per document

---
*This note was auto-generated after the analytics dashboard feature was added for future maintainers.*
# Batch Processing in ContentAnalyzer

## batch_analyze() method
- Added to `ContentAnalyzer` in `src/content_analyzer.py`.
- Processes multiple documents in a batch with:
  - Progress tracking (supports Streamlit's `st.progress()` via callback)
  - 0.5 second rate limiting between requests
  - Error handling (continues processing if one fails)
  - Returns results with document IDs and timestamps

## Usage Example

```python
from src.content_analyzer import ContentAnalyzer
import streamlit as st

def streamlit_progress(progress):
    st.progress(progress)

analyzer = ContentAnalyzer()
documents = [
    {'id': 'doc1', 'text': '...'},
    {'id': 'doc2', 'text': '...'},
]
results = analyzer.batch_analyze(documents, 'General Business', progress_callback=streamlit_progress)
```

## Notes
- Each result contains: `id`, `timestamp`, `result`, and `error` (if any).
- Designed for integration with Streamlit or other UI frameworks.
- See `src/content_analyzer.py` for implementation details.
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
