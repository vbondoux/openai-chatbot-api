import openai
import os
from app.config import OPENAI_API_KEY, UPLOADS_DIR

def upload_file_to_openai(filepath):
    """
    Upload un fichier stocké localement vers OpenAI Assistants API.
    Retourne l'ID du fichier stocké dans OpenAI.
    """
    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    try:
        with open(filepath, "rb") as file:
            response = client.files.create(
                file=file,
                purpose="assistants"
            )
        return response.id  # OpenAI renvoie un file_id
    except Exception as e:
        raise RuntimeError(f"Erreur lors de l'upload du fichier vers OpenAI : {e}")
