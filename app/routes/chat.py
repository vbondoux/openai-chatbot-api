from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, Field
import openai
from app.config import OPENAI_API_KEY

router = APIRouter()

# Initialisation du client OpenAI
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Modèle Pydantic pour les requêtes JSON
class ChatRequest(BaseModel):
    message: str = Field(..., example="Bonjour, peux-tu m'aider ?")

@router.post("/{assistant_id}/start")
async def start_chat_with_agent(
    assistant_id: str,
    body: ChatRequest = Body(...)
):
    """
    Démarre une conversation avec l'assistant et retourne immédiatement le thread_id et le run_id.
    """
    try:
        print(f"✅ Requête reçue : assistant_id={assistant_id}, message={body.message}")

        # Vérifier que l'assistant existe
        try:
            assistant = client.beta.assistants.retrieve(assistant_id)
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Assistant non trouvé : {str(e)}")

        # Créer un thread pour la conversation
        thread = client.beta.threads.create()

        # Ajouter le message utilisateur
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=body.message
        )

        # Démarrer l'exécution de l'assistant
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id
        )

        return {"thread_id": thread.id, "run_id": run.id}

    except Exception as e:
        print(f"❌ ERREUR : {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{thread_id}/status")
async def get_chat_status(thread_id: str):
    """
    Vérifie le statut du run en cours pour un thread donné.
    """
    try:
        runs = client.beta.threads.runs.list(thread_id=thread_id)

        if not runs.data:
            raise HTTPException(status_code=404, detail="Aucun run trouvé pour ce thread.")

        last_run = runs.data[0]

        return {"status": last_run.status}

    except Exception as e:
        print(f"❌ ERREUR : {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{thread_id}/response")
async def get_chat_response(thread_id: str):
    """
    Récupère la réponse de l'assistant une fois le run terminé.
    """
    try:
        runs = client.beta.threads.runs.list(thread_id=thread_id)
        if not runs.data or runs.data[0].status != "completed":
            return {"status": "in_progress", "message": "Le run est encore en cours, réessayez plus tard."}

        response_messages = client.beta.threads.messages.list(thread_id=thread_id)

        # ✅ Corrigé : extraire le dernier message de l'assistant uniquement
        for msg in reversed(response_messages.data):
            if msg.role == "assistant":
                reply = msg.content[0].text.value
                break
        else:
            reply = "Aucune réponse de l'assistant."

        return {"status": "completed", "response": reply}

    except Exception as e:
        print(f"❌ ERREUR : {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
