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

def attach_files_to_assistant(assistant_id, file_ids):
    """
    Associe une liste de fichiers (file_ids) à un assistant OpenAI en les ajoutant via update.
    """
    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    try:
        # ✅ Utiliser list_files pour récupérer les fichiers déjà attachés
        existing_files_response = client.beta.assistants.files.list(assistant_id=assistant_id)
        existing_files = [f.id for f in existing_files_response.data]

        # Fusionner les fichiers existants avec les nouveaux
        updated_files = list(set(existing_files + file_ids))

        # ✅ Ajouter les fichiers à l’assistant en plusieurs requêtes si nécessaire
        for file_id in file_ids:
            if file_id not in existing_files:
                client.beta.assistants.files.create(
                    assistant_id=assistant_id,
                    file_id=file_id
                )

        return {"message": "Fichiers attachés à l'assistant.", "file_ids": updated_files}
    except Exception as e:
        raise RuntimeError(f"Erreur lors de l'attachement des fichiers à l'assistant : {e}")
