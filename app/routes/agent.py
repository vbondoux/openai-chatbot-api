import openai
from fastapi import APIRouter, HTTPException
from app.config import OPENAI_API_KEY

router = APIRouter()

@router.post("/create")
def create_agent():
    """
    Crée un agent OpenAI pour l'aide à la décision en bourse.
    """
    try:
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
            model="gpt-4-turbo"
        )

        return {"assistant_id": assistant.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
