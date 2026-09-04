import os

import xml.etree.ElementTree as ET

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# --------------------------------------------------
# OpenAI summary
# --------------------------------------------------

def summarize_abstract(title, abstract):
    if not abstract:
        return "No abstract available."

    response = client.responses.create(
        model="gpt-5-mini",
        input=f"""
Summarize this scientific publication in 2-3 sentences.

Make it understandable to a general educated audience.
Focus on:
- what the researchers studied
- what they found
- why it matters

Do not invent information that is not present in the abstract.

Title:
{title}

Abstract:
{abstract}
"""
    )

    return response.output_text

