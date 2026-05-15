import os
import json

from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

google_credentials = os.getenv("GOOGLE_CREDENTIALS")

credentials_info = json.loads(google_credentials)

credentials = service_account.Credentials.from_service_account_info(
    credentials_info,
    scopes=SCOPES
)

service = build('drive', 'v3', credentials=credentials)


def search_drive(query):

    results = service.files().list(
        q=query,
        pageSize=10,
        fields="files(id, name, mimeType)"
    ).execute()

    items = results.get('files', [])

    return items