from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
import io
import os

def download_drive_file(file_id, output_path):
    """
    Télécharge un fichier depuis Google Drive via son file_id.
    """
    # Charger les credentials
    creds = service_account.Credentials.from_service_account_file(
        os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON"),
        scopes=["https://www.googleapis.com/auth/drive.readonly"],
    )

    # Construire le service Google Drive
    service = build("drive", "v3", credentials=creds)

    # Récupérer le fichier
    request = service.files().get_media(fileId=file_id)
    file = io.BytesIO()
    downloader = MediaIoBaseDownload(file, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Téléchargement {int(status.progress() * 100)}%")

    # Sauvegarder le fichier en local
    with open(output_path, "wb") as f:
        f.write(file.getvalue())

    return output_path
