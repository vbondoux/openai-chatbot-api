from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, Field
import openai
from app.config import OPENAI_API_KEY

router = APIRouter()

# Initialiser OpenAI API
openai.api_key = OPENAI_API_KEY

# Modèle pour JSON
class ChatRequest(BaseModel):
    message: str = Field(..., example="Bonjour, peux-tu m'aider ?")

@router.post("/{assistant_id}")
async def chat_with_agent(
    assistant_id: str,
    body: ChatRequest = Body(...)
):
    """
    Envoie un message à l'agent OpenAI et retourne la réponse.
    """
    try:
        print(f"✅ Requête reçue : assistant_id={assistant_id}, message={body.message}")

        # Simulation de réponse
        return {"response": f"Message bien reçu : {body.message}"}

    except Exception as e:
        print(f"❌ ERREUR : {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
