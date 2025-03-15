from fastapi import APIRouter, HTTPException
from app.utils.google_drive import download_drive_file
from pydantic import BaseModel
import os

router = APIRouter()

# Définition du modèle pour le body JSON
class DriveFileRequest(BaseModel):
    file_id: str

# Dossier où sont stockés les fichiers téléchargés
RAG_FILES_DIR = "/tmp/"  # Modifier si besoin

@router.post("/download_drive_file/")
def download_google_drive_file(request: DriveFileRequest):
    """
    Télécharge un fichier depuis Google Drive et retourne le chemin du fichier téléchargé.
    """
    try:
        file_id = request.file_id
        output_path = os.path.join(RAG_FILES_DIR, f"{file_id}.pdf")  # Modifier l'extension si besoin
        download_drive_file(file_id, output_path)
        return {"message": "Fichier téléchargé avec succès", "file_path": output_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload_from_drive/")
def upload_google_drive_file(request: DriveFileRequest):
    """
    Télécharge un fichier depuis Google Drive et retourne le chemin du fichier téléchargé.
    """
    try:
        file_id = request.file_id
        output_path = os.path.join(RAG_FILES_DIR, f"{file_id}.pdf")  # Modifier l'extension si besoin
        download_drive_file(file_id, output_path)
        return {"message": "Fichier téléchargé avec succès", "file_path": output_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list_rag_files/")
def list_rag_files():
    """
    Liste les fichiers disponibles dans la RAG.
    """
    try:
        files = [f for f in os.listdir(RAG_FILES_DIR) if os.path.isfile(os.path.join(RAG_FILES_DIR, f))]
        return {"rag_files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
