import openai
import os
import logging
from app.config import OPENAI_API_KEY, UPLOADS_DIR

# Initialisation du client OpenAI en forçant l'API Assistants v2
client = openai.OpenAI(
    api_key=OPENAI_API_KEY,
    default_headers={"OpenAI-Beta": "assistants=v2"}  # ✅ Activation explicite de l’API Assistants v2
)

# Configuration des logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def upload_file_to_openai(filepath):
    """Upload un fichier local vers OpenAI Assistants API et retourne son ID."""
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


def create_vector_store(name="Default Vector Store"):
    """Crée un Vector Store dans OpenAI Assistants API."""
    try:
        response = client.vector_stores.create(name=name)
        vector_store_id = response.id
        logging.info(f"✅ Vector Store créé avec succès ! ID : {vector_store_id}")
        return vector_store_id
    except Exception as e:
        logging.error(f"🚨 Erreur lors de la création du Vector Store : {e}")
        raise RuntimeError(f"Erreur lors de la création du Vector Store : {e}")


def add_file_to_vector_store(vector_store_id, file_id):
    """Ajoute un fichier à un Vector Store OpenAI."""
    try:
        logging.info(f"📎 Ajout du fichier {file_id} au Vector Store {vector_store_id}...")

        client.vector_stores.file_batches.create_and_poll(
            vector_store_id=vector_store_id,
            file_ids=[file_id]
        )
        logging.info(f"✅ Fichier {file_id} ajouté au Vector Store {vector_store_id}")
    except Exception as e:
        logging.error(f"🚨 Erreur lors de l'ajout du fichier au Vector Store : {e}")
        raise RuntimeError(f"Erreur lors de l'ajout du fichier au Vector Store : {e}")


def update_assistant_with_vector_store(assistant_id, vector_store_id):
    """Associe un Vector Store à un assistant OpenAI."""
    try:
        logging.info(f"🔗 Association du Vector Store {vector_store_id} avec l'assistant {assistant_id}...")

        client.beta.assistants.update(
            assistant_id=assistant_id,
            tool_resources={
                "file_search": {
                    "vector_store_ids": [vector_store_id]
                }
            }
        )

        logging.info(f"✅ L'assistant {assistant_id} est maintenant lié au Vector Store {vector_store_id}.")
    except Exception as e:
        logging.error(f"🚨 Erreur lors de la mise à jour de l'assistant avec le Vector Store : {e}")
        raise RuntimeError(f"Erreur lors de la mise à jour de l'assistant avec le Vector Store : {e}")


def upload_and_attach_files_to_rag(assistant_id):
    """Upload tous les fichiers locaux et les attache à l'assistant via un Vector Store."""
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

        vector_store_id = create_vector_store()
        for file_id in file_ids:
            add_file_to_vector_store(vector_store_id, file_id)

        update_assistant_with_vector_store(assistant_id, vector_store_id)

        logging.info(f"✅ Tous les fichiers ont été ajoutés et attachés avec succès !")
        return {"message": "Fichiers ajoutés et attachés avec succès.", "vector_store_id": vector_store_id}
    except Exception as e:
        logging.error(f"🚨 Erreur lors du processus d'upload et d'attachement des fichiers : {e}")
        raise RuntimeError(f"Erreur lors du processus d'upload et d'attachement des fichiers : {e}")


### NOUVELLES FONCTIONS POUR LES ROUTES

def list_assistants():
    """Récupère la liste de tous les assistants OpenAI."""
    try:
        response = client.beta.assistants.list()
        return [assistant.id for assistant in response.data]
    except Exception as e:
        logging.error(f"🚨 Erreur lors de la récupération des assistants : {e}")
        raise RuntimeError(f"Erreur lors de la récupération des assistants : {e}")


def get_assistant_details(assistant_id):
    """Récupère les détails d'un assistant spécifique."""
    try:
        response = client.beta.assistants.retrieve(assistant_id)
        return response
    except Exception as e:
        logging.error(f"🚨 Erreur lors de la récupération des détails de l'assistant : {e}")
        raise RuntimeError(f"Erreur lors de la récupération des détails de l'assistant : {e}")


def list_vector_store_files(assistant_id):
    """Récupère la liste des fichiers présents dans le Vector Store attaché à l'assistant."""
    try:
        assistant = get_assistant_details(assistant_id)
        vector_store_ids = assistant.tool_resources["file_search"]["vector_store_ids"]

        all_files = []
        for vector_store_id in vector_store_ids:
            response = client.vector_stores.files.list(vector_store_id=vector_store_id)
            all_files.extend(response.data)

        return [file.id for file in all_files]
    except Exception as e:
        logging.error(f"🚨 Erreur lors de la récupération des fichiers du Vector Store : {e}")
        raise RuntimeError(f"Erreur lors de la récupération des fichiers du Vector Store : {e}")
