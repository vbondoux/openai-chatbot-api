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
    Associe une liste de fichiers (file_ids) à un assistant OpenAI en les ajoutant un par un.
    """
    try:
        logging.info(f"🔍 Vérification des fichiers déjà attachés à l'assistant {assistant_id}...")

        # Récupérer les fichiers déjà attachés
        existing_files = client.beta.assistants.files.list(assistant_id=assistant_id).data
        existing_file_ids = [f.id for f in existing_files]
        logging.info(f"📄 Fichiers déjà attachés : {existing_file_ids}")

        # Ajouter les nouveaux fichiers si pas déjà attachés
        for file_id in file_ids:
            if file_id not in existing_file_ids:
                logging.info(f"📎 Attachement du fichier {file_id} à l'assistant {assistant_id}...")
                client.beta.assistants.files.create(
                    assistant_id=assistant_id,
                    file_id=file_id
                )
                logging.info(f"✅ Fichier {file_id} attaché avec succès !")
            else:
                logging.info(f"⚠️ Le fichier {file_id} est déjà attaché, on ignore.")

        return {"message": "Fichiers attachés à l'assistant.", "file_ids": file_ids}
    except Exception as e:
        logging.error(f"🚨 Erreur lors de l'attachement des fichiers à l'assistant : {e}")
        raise RuntimeError(f"Erreur lors de l'attachement des fichiers à l'assistant : {e}")

def upload_and_attach_files_to_rag(assistant_id):
    """
    Parcourt le dossier `uploads/`, envoie les fichiers à OpenAI et les attache à l'assistant.
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

        logging.info(f"📎 Attachement des fichiers à l'assistant {assistant_id}...")
        response = attach_files_to_assistant(assistant_id, file_ids)

        logging.info(f"✅ Tous les fichiers ont été attachés avec succès !")
        return response

    except Exception as e:
        logging.error(f"🚨 Erreur lors du processus d'upload et d'attachement des fichiers : {e}")
        raise RuntimeError(f"Erreur lors du processus d'upload et d'attachement des fichiers : {e}")
