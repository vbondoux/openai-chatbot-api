from fastapi import APIRouter, HTTPException, UploadFile, File, Form
import openai
import os
from app.config import OPENAI_API_KEY

router = APIRouter()

# Initialiser OpenAI API
openai.api_key = OPENAI_API_KEY

@router.post("/{assistant_id}")
async def chat_with_agent(
    assistant_id: str,
    message: str = Form(...), 
    file: UploadFile = File(None)
):
    """
    Envoie un message à l'agent OpenAI et retourne la réponse.
    """
    try:
        # Vérifier si un fichier est envoyé
        file_info = ""
        if file:
            file_location = f"/tmp/{file.filename}"
            with open(file_location, "wb") as buffer:
                buffer.write(await file.read())
            file_info = f"[Fichier joint: {file.filename}]"
        
        # Création d'un thread avec l'agent OpenAI
        thread = openai.beta.threads.create(
            messages=[
                {"role": "user", "content": f"{file_info} {message}"}
            ]
        )
        
        # Exécuter l'assistant pour obtenir une réponse
        run = openai.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )
        
        # Récupérer la réponse
        response = openai.beta.threads.messages.list(thread_id=thread.id)
        reply = response["data"][0]["content"]
        
        return {"response": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
