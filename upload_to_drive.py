from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
import json
import os

def upload_to_drive(file_path, folder_id):
    """Uploads a file to Google Drive"""
    creds_json = os.environ.get("GOOGLE_CREDENTIALS_JSON")
    if not creds_json:
        print("Google credentials not found!")
        return

    creds_dict = json.loads(creds_json)
    creds = Credentials.from_service_account_info(creds_dict)
    service = build("drive", "v3", credentials=creds)

    file_metadata = {"name": os.path.basename(file_path), "parents": [folder_id]}
    media = MediaFileUpload(file_path, mimetype="application/pdf")

    file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    print(f"Uploaded {file_path} to Google Drive with ID: {file.get('id')}")

if __name__ == "__main__":
    file_path = "example.pdf"
    folder_id = "YOUR_GOOGLE_DRIVE_FOLDER_ID"
    upload_to_drive(file_path, folder_id)
