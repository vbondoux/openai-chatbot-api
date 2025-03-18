from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Body, Depends
from pydantic import BaseModel, Field
import openai
import os
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
    message: str = Form(None),  # Supporte form-data
    file: UploadFile = File(None),  # Supporte fichiers
    body: ChatRequest = Body(None)  # Supporte JSON
):
    """
    Envoie un message à l'agent OpenAI et retourne la réponse.
    Fonctionne avec JSON ou `multipart/form-data`.
    """
    try:
        # LOG DES DONNÉES REÇUES
        print(f"✅ Requête reçue : assistant_id={assistant_id}, message={message}, body={body}")

        # Vérification et récupération du message
        if not message and body:
            message = body.message  # Extraction depuis JSON
        if not message:
            raise HTTPException(status_code=400, detail="Le message est requis.")

        # Gestion du fichier (optionnel)
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

        # Vérification de la réponse OpenAI
        messages = response.get("data", [])
        if not messages:
            raise HTTPException(status_code=500, detail="Aucune réponse de l'assistant.")
        
        reply = messages[0].get("content", "Réponse introuvable.")
        
        return {"response": reply}

    except Exception as e:
        print(f"❌ ERREUR : {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
