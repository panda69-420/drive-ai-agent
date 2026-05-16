import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv("../.env")

api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    groq_api_key=api_key,
    model_name="llama-3.1-8b-instant"
)

conversation_memory = []


def generate_drive_query(user_input):

    conversation_memory.append(user_input)

    lower_input = user_input.lower()

    query_parts = []

    # ---------- MIME TYPES ----------

    if "pdf" in lower_input:
        query_parts.append(
            "mimeType='application/pdf'"
        )

    if "spreadsheet" in lower_input or "sheets" in lower_input:
        query_parts.append(
            "mimeType='application/vnd.google-apps.spreadsheet'"
        )

    if "document" in lower_input or "doc" in lower_input:
        query_parts.append(
            "mimeType='application/vnd.google-apps.document'"
        )

    # ---------- RECENT / TIME ----------

    if "recent" in lower_input or "last week" in lower_input:

        last_week = (
            datetime.utcnow() - timedelta(days=7)
        ).strftime("%Y-%m-%dT00:00:00")

        query_parts.append(
            f"modifiedTime > '{last_week}'"
        )

    # ---------- REPORT KEYWORDS ----------

    keywords = [
        "report",
        "financial",
        "budget",
        "invoice"
    ]

    for word in keywords:
        if word in lower_input:
            query_parts.append(
                f"name contains '{word}'"
            )

    # ---------- FALLBACK TO LLM ----------

    if not query_parts:

        prompt = f"""
Convert this request into a valid Google Drive API q parameter.

Return ONLY the query.

User:
{user_input}
"""

        response = llm.invoke([
            HumanMessage(content=prompt)
        ])

        return response.content.strip()

    return " and ".join(query_parts)