import json
from pathlib import Path
import httpx
import streamlit as st

_config = json.loads((Path(__file__).parent.parent / "config.json").read_text())
BACKEND_URL = _config.get("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="YT Summarizer", page_icon="▶️", layout="centered")
st.title("YouTube Video Summarizer")

# Sidebar: optional API key override
with st.sidebar:
    st.header("Settings")
    api_key_input = st.text_input("OpenAI API Key (optional)", type="password",
                                  help="Overrides the OPENAI_API_KEY env var if provided.")

headers = {}
if api_key_input:
    headers["X-OpenAI-API-Key"] = api_key_input

# Step 1: Fetch transcript
st.subheader("Step 1 — Fetch Transcript")
url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Fetch Transcript"):
    if not url:
        st.error("Please enter a YouTube URL.")
    else:
        with st.spinner("Fetching transcript..."):
            try:
                resp = httpx.post(f"{BACKEND_URL}/api/transcript",
                                  json={"url": url}, headers=headers, timeout=30)
                if resp.status_code == 200:
                    data = resp.json()
                    st.session_state["transcript"] = data["transcript"]
                    st.session_state["video_id"] = data["video_id"]
                    st.success(f"Transcript fetched for video `{data['video_id']}`.")
                else:
                    st.error(resp.json().get("detail", "Failed to fetch transcript."))
                    st.session_state.pop("transcript", None)
            except Exception as e:
                st.error(f"Could not connect to backend: {e}")
                st.session_state.pop("transcript", None)

if "transcript" in st.session_state:
    with st.expander("View transcript"):
        st.write(st.session_state["transcript"])

    # Step 2: Summarize
    st.subheader("Step 2 — Summarize")
    format_map = {
        "Short Paragraph": "paragraph",
        "Key Bullet Points": "bullets",
        "Timestamped Chapters": "chapters",
    }
    selected_label = st.radio("Summary format", list(format_map.keys()), horizontal=True)

    if st.button("Summarize"):
        with st.spinner("Generating summary..."):
            try:
                resp = httpx.post(
                    f"{BACKEND_URL}/api/summarize",
                    json={"transcript": st.session_state["transcript"],
                          "format": format_map[selected_label]},
                    headers=headers,
                    timeout=60,
                )
                if resp.status_code == 200:
                    st.session_state["summary"] = resp.json()["summary"]
                else:
                    st.error(resp.json().get("detail", "Summarization failed."))
            except Exception as e:
                st.error(f"Could not connect to backend: {e}")

    if "summary" in st.session_state:
        st.markdown(st.session_state["summary"])

    # Step 3: Q&A
    st.subheader("Step 3 — Ask a Question")
    question = st.text_input("Your question about the video")

    if st.button("Ask"):
        if not question:
            st.error("Please enter a question.")
        else:
            with st.spinner("Thinking..."):
                try:
                    resp = httpx.post(
                        f"{BACKEND_URL}/api/ask",
                        json={"transcript": st.session_state["transcript"],
                              "question": question},
                        headers=headers,
                        timeout=60,
                    )
                    if resp.status_code == 200:
                        st.session_state["answer"] = resp.json()["answer"]
                    else:
                        st.error(resp.json().get("detail", "Q&A failed."))
                except Exception as e:
                    st.error(f"Could not connect to backend: {e}")

    if "answer" in st.session_state:
        st.markdown("**Answer:**")
        st.write(st.session_state["answer"])
