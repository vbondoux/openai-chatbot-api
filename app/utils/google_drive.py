from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
import io
import os
from app.config import GOOGLE_CREDENTIALS_PATH, UPLOADS_DIR

def download_drive_file(file_id, output_path=None):
    """
    Télécharge un fichier depuis Google Drive via son file_id.
    """
    # Vérifier si les credentials existent
    if not GOOGLE_CREDENTIALS_PATH or not os.path.exists(GOOGLE_CREDENTIALS_PATH):
        raise FileNotFoundError(f"❌ Fichier credentials introuvable : {GOOGLE_CREDENTIALS_PATH}")

    # Charger les credentials
    creds = service_account.Credentials.from_service_account_file(
        GOOGLE_CREDENTIALS_PATH,
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

    # Déterminer le chemin de sortie
    if not output_path:
        output_path = os.path.join(UPLOADS_DIR, f"{file_id}.pdf")

    # Sauvegarder le fichier en local
    with open(output_path, "wb") as f:
        f.write(file.getvalue())

    return output_path
