import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv("../.env")

api_key = os.getenv("GROQ_API_KEY")

print("API KEY LOADED:", api_key is not None)

llm = ChatGroq(
    groq_api_key=api_key,
    model_name="llama-3.1-8b-instant"
)


def generate_drive_query(user_input):

    prompt = f"""
    You are a Google Drive query generator.

    Convert the user's request into a valid Google Drive API q parameter.

    Examples:

    User: Find PDF files
    Output:
    mimeType='application/pdf'

    User: Find reports
    Output:
    name contains 'report'

    User: Find spreadsheets
    Output:
    mimeType='application/vnd.google-apps.spreadsheet'

    Return ONLY the query.
    No explanation.

    User Request:
    {user_input}
    """

    response = llm.invoke([
        HumanMessage(content=prompt)
    ])

    return response.content.strip()