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


def answer_question(transcript: str, question: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Answer questions using only the provided transcript.",
            },
            {
                "role": "user",
                "content": f"Transcript:\n\n{transcript}\n\nQuestion: {question}",
            },
        ],
    )
    return response.choices[0].message.content
