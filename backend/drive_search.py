import os
import json

from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv("../.env")

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

# Try Render environment variable first
google_credentials = os.getenv("GOOGLE_CREDENTIALS")

if google_credentials:

    credentials_info = json.loads(google_credentials)

    credentials = service_account.Credentials.from_service_account_info(
        credentials_info,
        scopes=SCOPES
    )

else:
    # Local fallback using credentials.json
    credentials = service_account.Credentials.from_service_account_file(
        "credentials.json",
        scopes=SCOPES
    )

service = build('drive', 'v3', credentials=credentials)


def search_drive(query):

    results = service.files().list(
        q=query,
        pageSize=10,
        fields="files(id, name, mimeType, modifiedTime)"
    ).execute()

    items = results.get('files', [])

    return items