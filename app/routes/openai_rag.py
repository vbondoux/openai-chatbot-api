import os
import requests
from fastapi import APIRouter, HTTPException
from app.config import OPENAI_API_KEY, UPLOADS_DIR

router = APIRouter()

OPENAI_ASSISTANT_ID = "ton_assistant_id"  # Remplace par l'ID réel de ton agent

@router.post("/openai/upload_file/")
def upload_file_to_openai(file_name: str):
    """
    Upload un fichier stocké dans UPLOADS_DIR vers OpenAI Assistants API.
    """
    file_path = os.path.join(UPLOADS_DIR, file_name)

    # Vérifier si le fichier existe
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Fichier introuvable : {file_path}")

    try:
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
        files = {"file": open(file_path, "rb")}
        
        response = requests.post("https://api.openai.com/v1/files", headers=headers, files=files)
        response_data = response.json()

        if "id" in response_data:
            return {"message": "Fichier uploadé vers OpenAI", "file_id": response_data["id"]}
        else:
            raise HTTPException(status_code=500, detail=f"Erreur OpenAI : {response_data}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
      
@router.post("/openai/attach_file/")
def attach_file_to_assistant(file_id: str):
    """
    Associe un fichier OpenAI à l’agent OpenAI.
    """
    try:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }
        data = {"file_id": file_id}

        response = requests.post(
            f"https://api.openai.com/v1/assistants/{OPENAI_ASSISTANT_ID}/files",
            headers=headers,
            json=data
        )

        response_data = response.json()

        if "id" in response_data:
            return {"message": "Fichier attaché à l’assistant", "assistant_file_id": response_data["id"]}
        else:
            raise HTTPException(status_code=500, detail=f"Erreur OpenAI : {response_data}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
