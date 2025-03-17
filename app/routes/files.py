from fastapi import APIRouter, HTTPException
import os
from app.utils.google_drive import (
    download_drive_file,
    list_drive_files,
    download_missing_drive_files
)
from app.utils.openai_rag import (
    upload_file_to_openai, 
    upload_and_attach_files_to_rag, 
    list_assistants, 
    list_vector_store_files, 
    get_assistant_details,
    remove_assistant
)
from app.routes.agent import get_assistant_id  # ✅ Utilisation de la nouvelle fonction
from pydantic import BaseModel
from app.config import UPLOADS_DIR

router = APIRouter()

class DriveFileRequest(BaseModel):
    file_id: str

@router.post("/upload_from_drive/")
def upload_google_drive_file(request: DriveFileRequest):
    """
    Télécharge un fichier depuis Google Drive, l'upload vers OpenAI et retourne les informations.
    """
    try:
        file_path, filename = download_drive_file(request.file_id)

        # On récupère l'ID de l'assistant
        assistant_id = get_assistant_id()
        if not assistant_id:
            raise HTTPException(status_code=400, detail="❌ Aucun assistant trouvé. Créez-en un d'abord !")

        # On upload le fichier sur OpenAI
        file_id = upload_file_to_openai(file_path)

        return {"message": "Fichier téléchargé et uploadé avec succès", "file_name": filename, "file_id": file_id}
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
    Upload tous les fichiers stockés localement dans /uploads vers OpenAI Assistants API 
    et les associe à l'assistant via Vector Store.
    """
    try:
        assistant_id = get_assistant_id()  # ✅ Utilisation de la nouvelle fonction
        if not assistant_id:
            raise HTTPException(status_code=400, detail="❌ Aucun assistant trouvé. Créez-en un d'abord !")

        response = upload_and_attach_files_to_rag(assistant_id)
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list_assistants/")
def get_all_assistants():
    """ Récupère la liste de tous les assistants OpenAI créés. """
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
        assistant_id = get_assistant_id()
        if not assistant_id:
            raise HTTPException(status_code=400, detail="❌ Aucun assistant trouvé. Créez-en un d'abord !")

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
        assistant_id = get_assistant_id()
        if not assistant_id:
            raise HTTPException(status_code=400, detail="❌ Aucun assistant trouvé. Créez-en un d'abord !")

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
        return {"message": f"✅ Assistant {assistant_id} supprimé avec succès.", "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list_drive_files/")
def get_drive_files():
    """
    Récupère la liste des fichiers disponibles dans un dossier spécifique de Google Drive.
    """
    try:
        drive_files = list_drive_files()
        return {"drive_files": drive_files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload_all_from_drive/")
def upload_all_drive_files():
    """
    Télécharge tous les fichiers depuis un dossier Google Drive vers le stockage local sur Railway,
    en évitant les fichiers déjà présents.
    """
    try:
        result = download_missing_drive_files()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
