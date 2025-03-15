from fastapi import APIRouter, HTTPException
import os
from app.utils.google_drive import download_drive_file
from app.utils.openai_rag import (
    upload_file_to_openai, 
    upload_and_attach_files_to_rag, 
    list_assistants, 
    list_vector_store_files, 
    get_assistant_details
)
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
    Upload tous les fichiers stockés localement dans /uploads vers OpenAI Assistants API et les associe à l'assistant via Vector Store.
    """
    try:
        assistant_id = load_assistant_id()
        if not assistant_id:
            raise HTTPException(status_code=400, detail="L'assistant OpenAI n'a pas été créé.")

        response = upload_and_attach_files_to_rag(assistant_id)
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list_assistants/")
def get_all_assistants():
    """
    Récupère la liste de tous les assistants OpenAI créés.
    """
    try:
        assistants = list_assistants()
        return {"assistants": assistants}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list_vector_store_files/")
def get_vector_store_files():
    """
    Récupère la liste des fichiers présents dans le Vector Store attaché à l'assistant OpenAI.
    """
    try:
        assistant_id = load_assistant_id()
        if not assistant_id:
            raise HTTPException(status_code=400, detail="L'assistant OpenAI n'a pas été créé.")

        files = list_vector_store_files(assistant_id)
        return {"vector_store_files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/assistant_details/")
def get_assistant_info():
    """
    Récupère les détails de l'assistant OpenAI, y compris son Vector Store.
    """
    try:
        assistant_id = load_assistant_id()
        if not assistant_id:
            raise HTTPException(status_code=400, detail="L'assistant OpenAI n'a pas été créé.")

        assistant_details = get_assistant_details(assistant_id)
        return {"assistant_details": assistant_details}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete_assistant/{assistant_id}")
def delete_assistant(assistant_id: str):
    """
    Supprime un assistant OpenAI via son ID.
    """
    try:
        response = remove_assistant(assistant_id)
        return {"message": f"Assistant {assistant_id} supprimé avec succès.", "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

