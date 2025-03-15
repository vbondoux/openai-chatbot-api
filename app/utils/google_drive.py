from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
import io
import os
from app.config import GOOGLE_SERVICE_ACCOUNT_JSON  # Assurez-vous que cette variable est bien définie

# Définition du dossier de stockage des fichiers
RAG_FILES_DIR = "/tmp/"  # Modifier si nécessaire

def download_drive_file(file_id, output_path):
    """
    Télécharge un fichier depuis Google Drive via son file_id et l'enregistre en local.
    """
    try:
        # Vérifier si les credentials existent
        if not GOOGLE_SERVICE_ACCOUNT_JSON or not os.path.exists(GOOGLE_SERVICE_ACCOUNT_JSON):
            raise FileNotFoundError(f"❌ Fichier credentials introuvable : {GOOGLE_SERVICE_ACCOUNT_JSON}")

        # Charger les credentials
        creds = service_account.Credentials.from_service_account_file(
            GOOGLE_SERVICE_ACCOUNT_JSON,
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

        # Vérifier et créer le dossier si nécessaire
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Sauvegarder le fichier en local
        with open(output_path, "wb") as f:
            f.write(file.getvalue())

        print(f"✅ Fichier téléchargé et sauvegardé : {output_path}")

        return output_path

    except Exception as e:
        print(f"❌ Erreur lors du téléchargement du fichier : {e}")
        raise
