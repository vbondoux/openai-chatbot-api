import openai
from fastapi import APIRouter, HTTPException
from app.config import OPENAI_API_KEY

router = APIRouter()

@router.post("/create")
def create_agent():
    """
    Crée un agent OpenAI avec un prompt d’instructions et retourne son ID.
    """
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)

        assistant = client.beta.assistants.create(
            name="Mon Agent OpenAI",
            instructions="Tu es un assistant intelligent qui aide les utilisateurs.",
            model="gpt-4-turbo"
        )

        return {"assistant_id": assistant.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
