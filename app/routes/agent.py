import openai
import json
import os
from fastapi import APIRouter, HTTPException
from app.config import OPENAI_API_KEY

router = APIRouter()

# Fichier où stocker l'ID de l'assistant
ASSISTANT_DATA_FILE = "assistant_data.json"

def get_assistant_id():
    """Retourne l'ID de l'assistant s'il existe, sinon None."""
    if os.path.exists(ASSISTANT_DATA_FILE):
        with open(ASSISTANT_DATA_FILE, "r") as f:
            data = json.load(f)
            return data.get("assistant_id")
    return None

def save_assistant_id(assistant_id):
    """Sauvegarde l'ID de l'assistant dans un fichier JSON."""
    with open(ASSISTANT_DATA_FILE, "w") as f:
        json.dump({"assistant_id": assistant_id}, f)

@router.post("/create")
def create_agent():
    """
    Crée un agent OpenAI pour l'aide à la décision en bourse, ou retourne l'ID s'il existe déjà.
    """
    try:
        assistant_id = get_assistant_id()
        if assistant_id:
            return {"message": "Assistant déjà créé", "assistant_id": assistant_id}

        client = openai.OpenAI(api_key=OPENAI_API_KEY)

        instructions = """
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
        """

        assistant = client.beta.assistants.create(
            name="Aide à la Décision Boursière",
            instructions=instructions,
            model="gpt-4-turbo",
            {"type": "retrieval"},
            {"type": "file_search"}] 
        )

        save_assistant_id(assistant.id)
        return {"message": "Assistant créé avec succès", "assistant_id": assistant.id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
