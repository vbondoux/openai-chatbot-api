from fastapi import APIRouter, HTTPException
import os
from app.utils.google_drive import download_drive_file
from app.utils.openai_rag import upload_file_to_openai, upload_and_attach_files_to_assistant
from app.routes.agent import load_assistant_id
from pydantic import BaseModel
from app.config import UPLOADS_DIR

router = APIRouter()

# Définition du modèle pour le body JSON
class DriveFileRequest(BaseModel):
    file_id: str

@router.post("/download_drive_file/")
def download_google_drive_file(request: DriveFileRequest):
    """
    Télécharge un fichier depuis Google Drive et retourne son nom d'origine et son chemin.
    """
    try:
        file_path, filename = download_drive_file(request.file_id)
        return {"message": "Fichier téléchargé avec succès", "file_name": filename, "file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload_from_drive/")
def upload_google_drive_file(request: DriveFileRequest):
    """
    Télécharge un fichier depuis Google Drive et retourne son nom d'origine et son chemin.
    """
    try:
        file_path, filename = download_drive_file(request.file_id)
        return {"message": "Fichier téléchargé avec succès", "file_name": filename, "file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list_rag_files/")
def list_rag_files():
    """
    Liste les fichiers disponibles dans la RAG.
    """
    try:
        files = [f for f in os.listdir(UPLOADS_DIR) if os.path.isfile(os.path.join(UPLOADS_DIR, f))]
        return {"rag_files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload_to_rag/")
def upload_local_files_to_openai():
    """
    Upload tous les fichiers stockés localement dans /uploads vers OpenAI Assistants API et les associe à l'assistant.
    """
    try:
        assistant_id = load_assistant_id()
        if not assistant_id:
            raise HTTPException(status_code=400, detail="L'assistant OpenAI n'a pas été créé.")

        # ✅ Nouvelle approche : on envoie tout à OpenAI en une seule fonction
        response = upload_and_attach_files_to_assistant(assistant_id)

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
