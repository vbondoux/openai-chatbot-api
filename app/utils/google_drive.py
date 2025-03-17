from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
import io
import os
from app.config import GOOGLE_CREDENTIALS_PATH, UPLOADS_DIR,GOOGLE_DRIVE_FOLDER_ID

def download_drive_file(file_id):
    """
    Télécharge un fichier depuis Google Drive via son file_id et conserve son nom d'origine.
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

    # Obtenir le nom du fichier
    file_metadata = service.files().get(fileId=file_id).execute()
    filename = file_metadata.get("name", f"{file_id}.pdf")  # Fallback au file_id si aucun nom n'est trouvé

    # Récupérer le fichier
    request = service.files().get_media(fileId=file_id)
    file = io.BytesIO()
    downloader = MediaIoBaseDownload(file, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Téléchargement {int(status.progress() * 100)}%")

    # Sauvegarder le fichier dans UPLOADS_DIR
    output_path = os.path.join(UPLOADS_DIR, filename)
    with open(output_path, "wb") as f:
        f.write(file.getvalue())

    return output_path, filename

def list_drive_files():
    """
    Liste tous les fichiers disponibles dans un dossier spécifique de Google Drive.
    """
    # Vérifier les credentials
    if not GOOGLE_CREDENTIALS_PATH or not os.path.exists(GOOGLE_CREDENTIALS_PATH):
        raise FileNotFoundError(f"❌ Fichier credentials introuvable : {GOOGLE_CREDENTIALS_PATH}")

    # Authentification Google Drive
    creds = service_account.Credentials.from_service_account_file(
        GOOGLE_CREDENTIALS_PATH,
        scopes=["https://www.googleapis.com/auth/drive.readonly"],
    )

    service = build("drive", "v3", credentials=creds)

    # Vérifier si l'ID du dossier est bien défini
    if not GOOGLE_DRIVE_FOLDER_ID:
        raise ValueError("❌ Aucun dossier Google Drive spécifié dans Railway.")

    # Filtrer les fichiers par dossier
    query = f"'{GOOGLE_DRIVE_FOLDER_ID}' in parents and trashed=false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get("files", [])

    return [{"id": file["id"], "name": file["name"]} for file in files]
    
def download_missing_drive_files():
    """
    Télécharge uniquement les fichiers qui ne sont pas déjà présents dans le dossier UPLOADS_DIR.
    """
    try:
        drive_files = list_drive_files()  # Liste des fichiers du dossier Drive
        local_files = set(os.listdir(UPLOADS_DIR))  # Liste des fichiers déjà téléchargés

        downloaded_files = []
        skipped_files = []

        for file in drive_files:
            file_name = file["name"]
            file_id = file["id"]

            if file_name in local_files:
                skipped_files.append(file_name)  # Fichier déjà présent
            else:
                file_path, _ = download_drive_file(file_id)  # Téléchargement
                downloaded_files.append(file_name)

        return {"downloaded": downloaded_files, "skipped": skipped_files}
    except Exception as e:
        raise RuntimeError(f"🚨 Erreur lors du téléchargement des fichiers : {e}")


