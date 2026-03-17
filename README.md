YT Summarizer

  A FastAPI-powered backend that extracts and summarizes YouTube video transcripts using
  Azure OpenAI (GPT-4.1 Mini), with a Streamlit frontend.

  Features:
  - Transcript extraction — Fetches captions from any YouTube video URL (standard, short,
   and youtu.be links)
  - Summarization — Generates summaries in three formats: paragraph, bullet points, or
  chapter breakdowns
  - Q&A — Answers natural language questions grounded strictly in the video's transcript

  Tech stack: Python · FastAPI · Streamlit · Azure OpenAI · youtube-transcript-api

  API Endpoints

POST /api/transcript — Fetch transcript from a YouTube URL
POST /api/summarize — Summarize a transcript (paragraph / bullets / chapters)
POST /api/ask — Ask a question about the transcript

  ---
  Getting Started

  Prerequisites

  - Python 3.10+
  - An Azure OpenAI resource with a deployed model

  1. Clone the repository

  git clone <repo-url>
  cd yt-summarizer

  2. Create and activate a virtual environment

  python -m venv venv
  source venv/bin/activate        # macOS/Linux
  venv\Scripts\activate           # Windows

  3. Install dependencies

  pip install -r requirements.txt

  4. Configure credentials

  Create a config.json file in the project root:
  {
      "api_key": "your-azure-openai-api-key",
      "azure_endpoint": "https://your-resource.cognitiveservices.azure.com/",
      "api_version": "2024-12-01-preview"
  }

  5. Run the backend

  cd backend
  uvicorn main:app --reload
  The API will be available at http://localhost:8000.

  6. Run the frontend

  In a separate terminal (from the project root):
  streamlit run frontend/app.py
  The UI will open at http://localhost:8501.
