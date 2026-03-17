import json
import os
from openai import AzureOpenAI

_config_path = os.path.join(os.path.dirname(__file__), "..", "..", "config.json")
with open(_config_path) as _f:
    _config = json.load(_f)

client = AzureOpenAI(
    api_key=_config["api_key"],
    azure_endpoint=_config["azure_endpoint"],
    api_version=_config["api_version"],
)

FORMAT_INSTRUCTIONS = {
    "paragraph": "Write a concise 3-5 sentence summary of the video content.",
    "bullets": "List 5-10 key takeaways from the video as bullet points.",
    "chapters": "Break the content into titled sections with approximate timestamps based on the transcript.",
}


def summarize(transcript: str, format: str) -> str:
    instruction = FORMAT_INSTRUCTIONS[format]
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": instruction},
            {"role": "user", "content": f"Transcript:\n\n{transcript}"},
        ],
    )
    return response.choices[0].message.content
