from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Body
from pydantic import BaseModel
import openai
import os
from app.config import OPENAI_API_KEY

router = APIRouter()

# Initialiser OpenAI API
openai.api_key = OPENAI_API_KEY

# Modèle pour accepter JSON
class ChatRequest(BaseModel):
    message: str

@router.post("/{assistant_id}")
async def chat_with_agent(
    assistant_id: str,
    message: str = Form(None),  # Pour les requêtes `multipart/form-data`
    file: UploadFile = File(None),  # Fichier optionnel
    body: ChatRequest = Body(None)  # Pour les requêtes JSON
):
    """
    Envoie un message à l'agent OpenAI et retourne la réponse.
    Fonctionne avec ou sans fichier attaché.
    """
    try:
        # Récupération correcte du message
        if not message and body:
            message = body.message  # Si JSON, on extrait depuis le body
        if not message:
            raise HTTPException(status_code=400, detail="Le message est requis.")

        # Gestion du fichier
        file_info = ""
        if file:
            file_location = f"/tmp/{file.filename}"
            with open(file_location, "wb") as buffer:
                buffer.write(await file.read())
            file_info = f"[Fichier reçu: {file.filename}]"

        # Création d'un thread OpenAI
        thread = openai.beta.threads.create(
            messages=[
                {"role": "user", "content": f"{file_info} {message}"}
            ]
        )

        # Exécuter l'assistant
        run = openai.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )

        # Attendre et récupérer la réponse
        response = openai.beta.threads.messages.list(thread_id=thread.id)

        # 🔹 Nouvelle correction : extraire correctement la réponse
        messages = response.get("data", [])
        if not messages:
            raise HTTPException(status_code=500, detail="Aucune réponse de l'assistant.")
        
        reply = messages[0].get("content", "Réponse introuvable.")
        
        return {"response": reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
