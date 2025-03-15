import openai
import os
import logging
from app.config import OPENAI_API_KEY, UPLOADS_DIR

# Initialisation du client OpenAI
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Configuration des logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def upload_file_to_openai(filepath):
    """
    Upload un fichier stocké localement vers OpenAI Assistants API.
    Retourne l'ID du fichier stocké dans OpenAI.
    """
    try:
        logging.info(f"📤 Début de l'upload du fichier : {filepath}")

        if not os.path.exists(filepath):
            logging.error(f"❌ Le fichier {filepath} n'existe pas !")
            raise FileNotFoundError(f"Le fichier {filepath} est introuvable.")

        with open(filepath, "rb") as file:
            response = client.files.create(
                file=file,
                purpose="assistants"
            )

        file_id = response.id
        logging.info(f"✅ Fichier uploadé avec succès ! ID OpenAI : {file_id}")

        return file_id
    except Exception as e:
        logging.error(f"🚨 Erreur lors de l'upload du fichier vers OpenAI : {e}")
        raise RuntimeError(f"Erreur lors de l'upload du fichier vers OpenAI : {e}")

def attach_files_to_assistant(assistant_id, file_ids):
    """
    Attache directement les fichiers uploadés à l'assistant OpenAI.
    """
    try:
        logging.info(f"📎 Attachement des fichiers {file_ids} à l'assistant {assistant_id}...")

        # Associer les fichiers à l'assistant
        client.beta.assistants.update(
            assistant_id,
            file_ids=file_ids
        )

        logging.info(f"✅ Fichiers attachés avec succès à l'assistant {assistant_id}.")
        return {"message": "Fichiers attachés avec succès.", "file_ids": file_ids}
    except Exception as e:
        logging.error(f"🚨 Erreur lors de l'attachement des fichiers à l'assistant : {e}")
        raise RuntimeError(f"Erreur lors de l'attachement des fichiers à l'assistant : {e}")

def upload_and_attach_files_to_assistant(assistant_id):
    """
    Upload tous les fichiers stockés localement dans /uploads vers OpenAI Assistants API et les attache à l'assistant.
    """
    try:
        logging.info(f"📂 Parcours du dossier des fichiers à envoyer : {UPLOADS_DIR}")

        if not os.path.exists(UPLOADS_DIR):
            logging.error(f"❌ Dossier {UPLOADS_DIR} introuvable !")
            raise FileNotFoundError(f"Le dossier {UPLOADS_DIR} est introuvable.")

        file_ids = []
        for filename in os.listdir(UPLOADS_DIR):
            file_path = os.path.join(UPLOADS_DIR, filename)
            logging.info(f"📤 Upload du fichier : {file_path}")
            file_id = upload_file_to_openai(file_path)
            file_ids.append(file_id)

        if not file_ids:
            logging.warning("⚠️ Aucun fichier trouvé à uploader.")
            return {"message": "Aucun fichier trouvé dans le dossier uploads."}

        # Attachement direct des fichiers à l'assistant
        response = attach_files_to_assistant(assistant_id, file_ids)

        logging.info(f"✅ Tous les fichiers ont été attachés avec succès à l'assistant !")
        return response
    except Exception as e:
        logging.error(f"🚨 Erreur lors du processus d'upload et d'attachement des fichiers : {e}")
        raise RuntimeError(f"Erreur lors du processus d'upload et d'attachement des fichiers : {e}")
