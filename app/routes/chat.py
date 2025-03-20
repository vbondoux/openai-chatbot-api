from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, Field
import openai
from app.config import OPENAI_API_KEY

router = APIRouter()

# Initialiser OpenAI API
client = openai.OpenAI(api_key=OPENAI_API_KEY)

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

        # Étape 1 : Créer un thread pour la conversation
        thread = client.beta.threads.create()

        # Étape 2 : Envoyer le message dans le thread
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=body.message
        )

        # Étape 3 : Exécuter l'assistant sur ce thread
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )

        # **IMPORTANT** : Attendre que le run soit terminé avant de récupérer les messages
        import time
        while True:
            run_status = client.beta.threads.runs.retrieve(run.id)
            if run_status.status == "completed":
                break
            time.sleep(1)  # Attendre 1 seconde avant de re-vérifier

        # Étape 4 : Récupérer la réponse générée
        response_messages = client.beta.threads.messages.list(thread_id=thread.id)

        # Extraire le dernier message
        if response_messages and len(response_messages.data) > 0:
            reply = response_messages.data[0].content[0].text.value  # 🔥 CORRECTION ICI 🔥
        else:
            reply = "Aucune réponse de l'assistant."

        return {"response": reply}

    except Exception as e:
        print(f"❌ ERREUR : {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
