import os
import json
import requests
from fastapi import APIRouter, HTTPException
from app.config import OPENAI_API_KEY, save_assistant_id, load_assistant_id

router = APIRouter()

@router.post("/agent/create")
def create_openai_agent():
    """
    Crée un assistant OpenAI et stocke son assistant_id.
    Si un assistant existe déjà, il est réutilisé.
    """
    try:
        # Vérifier si un assistant existe déjà
        existing_assistant_id = load_assistant_id()
        if existing_assistant_id:
            return {"message": "Assistant déjà créé", "assistant_id": existing_assistant_id}

        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }

        data = {
            "name": "ProfitPulse AI",
            "instructions": "Tu es un assistant IA spécialisé en gestion de documents et en intelligence artificielle.",
            "tools": [{"type": "retrieval"}],  # Activation du RAG
            "model": "gpt-4-turbo"
        }

        response = requests.post("https://api.openai.com/v1/assistants", headers=headers, json=data)
        response_data = response.json()

        if "id" in response_data:
            assistant_id = response_data["id"]
            save_assistant_id(assistant_id)  # Sauvegarde l’ID
            return {"message": "Assistant créé avec succès", "assistant_id": assistant_id}
        else:
            raise HTTPException(status_code=500, detail=f"Erreur OpenAI : {response_data}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
