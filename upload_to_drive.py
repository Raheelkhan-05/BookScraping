from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
import json
import os
import sys

def upload_to_drive(file_path, folder_id):
    """Uploads a file to Google Drive and prints details"""

    # Load credentials from environment
    creds_json = os.environ.get("GOOGLE_CREDENTIALS_JSON")
    if not creds_json:
        print("❌ Google credentials not found in environment variable 'GOOGLE_CREDENTIALS_JSON'")
        return

    try:
        creds_dict = json.loads(creds_json)
        creds = Credentials.from_service_account_info(creds_dict)
        service = build("drive", "v3", credentials=creds)
    except Exception as e:
        print(f"❌ Failed to authenticate: {e}")
        return

    if not os.path.isfile(file_path):
        print(f"❌ File not found: {file_path}")
        return

    # Prepare file metadata and upload
    try:
        file_metadata = {
            "name": os.path.basename(file_path),
            "parents": [folder_id]
        }
        media = MediaFileUpload(file_path, resumable=True)

        uploaded_file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id, parents"
        ).execute()

        file_id = uploaded_file["id"]
        file_url = f"https://drive.google.com/file/d/{file_id}/view"

        # Get uploader account
        file_info = service.files().get(fileId=file_id, fields="owners(emailAddress)").execute()
        owner_email = file_info["owners"][0]["emailAddress"]

        print(f"✅ Uploaded: {file_path}")
        print(f"📁 Folder ID: {folder_id}")
        print(f"🔗 File URL: {file_url}")
        print(f"👤 Uploaded by: {owner_email}")

    except Exception as e:
        print(f"❌ Upload failed: {e}")

if __name__ == "__main__":
    # You can replace these or pass via command line
    file_path = "example.pdf"
    folder_id = "YOUR_GOOGLE_DRIVE_FOLDER_ID"

    # Optional: allow command-line override
    if len(sys.argv) == 3:
        file_path = sys.argv[1]
        folder_id = sys.argv[2]

    upload_to_drive(file_path, folder_id)
