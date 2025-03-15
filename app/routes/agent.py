import os
import json
import requests
from fastapi import APIRouter, HTTPException
from app.config import OPENAI_API_KEY

router = APIRouter()

ASSISTANT_ID_FILE = "assistant_id.json"

def save_assistant_id(assistant_id):
    """ Sauvegarde l'ID de l'assistant OpenAI dans un fichier JSON. """
    with open(ASSISTANT_ID_FILE, "w") as f:
        json.dump({"assistant_id": assistant_id}, f)

def load_assistant_id():
    """ Charge l'ID de l'assistant s'il a déjà été créé. """
    if os.path.exists(ASSISTANT_ID_FILE):
        with open(ASSISTANT_ID_FILE, "r") as f:
            return json.load(f).get("assistant_id")
    return None

@router.post("/agent/create/")
def create_agent():
    """
    Crée un agent OpenAI pour l'aide à la décision en bourse.
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
            "instructions": """
                Tu es un assistant spécialisé en analyse boursière et en intelligence artificielle.
                Ton objectif est d'aider les investisseurs à prendre des décisions éclairées.

                Tu es basé sur les expertises suivantes :
                - Uri : Expert en bourse, connaissant les tendances des marchés financiers et les stratégies d'investissement.
                - Vincent : Chef de projet senior, spécialisé en innovation IA et automatisation des processus financiers.
                - Sami : Ingénieur NLP, expert en traitement du langage naturel pour analyser des tendances du marché et extraire des insights.

                Tu dois répondre aux questions des utilisateurs en combinant :
                - Analyse des tendances boursières.
                - Approches basées sur l'intelligence artificielle et l'automatisation.
                - Explication des modèles NLP appliqués aux marchés financiers.

                Tu es rigoureux, précis et tu expliques tes analyses de manière claire.
            """,
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
