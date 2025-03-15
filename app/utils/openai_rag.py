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

def create_vector_store(name="Default Vector Store", description="Stockage des fichiers pour l'Assistant OpenAI"):
    """
    Crée un Vector Store dans OpenAI.
    """
    try:
        response = client.beta.vector_stores.create(
            name=name,
            description=description
        )
        vector_store_id = response.id
        logging.info(f"✅ Vector Store créé avec succès ! ID : {vector_store_id}")
        return vector_store_id
    except Exception as e:
        logging.error(f"🚨 Erreur lors de la création du Vector Store : {e}")
        raise RuntimeError(f"Erreur lors de la création du Vector Store : {e}")

def add_file_to_vector_store(vector_store_id, file_id):
    """
    Ajoute un fichier à un Vector Store.
    """
    try:
        logging.info(f"📎 Ajout du fichier {file_id} au Vector Store {vector_store_id}...")
        
        client.beta.vector_stores.file_batches.create_and_poll(
            vector_store_id=vector_store_id,
            file_ids=[file_id]
        )
        logging.info(f"✅ Fichier {file_id} ajouté au Vector Store {vector_store_id}")
    except Exception as e:
        logging.error(f"🚨 Erreur lors de l'ajout du fichier au Vector Store : {e}")
        raise RuntimeError(f"Erreur lors de l'ajout du fichier au Vector Store : {e}")

def update_assistant_with_vector_store(assistant_id, vector_store_id):
    """
    Associe un Vector Store à un assistant OpenAI.
    """
    try:
        logging.info(f"🔗 Association du Vector Store {vector_store_id} avec l'assistant {assistant_id}...")

        client.beta.assistants.update(
            assistant_id,
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
    """
    Parcourt le dossier `uploads/`, envoie les fichiers à OpenAI et les attache à l'assistant via un Vector Store.
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

        # Création du Vector Store et ajout des fichiers
        vector_store_id = create_vector_store()
        for file_id in file_ids:
            add_file_to_vector_store(vector_store_id, file_id)

        # Mise à jour de l'assistant avec le Vector Store
        update_assistant_with_vector_store(assistant_id, vector_store_id)

        logging.info(f"✅ Tous les fichiers ont été ajoutés et attachés avec succès !")
        return {"message": "Fichiers ajoutés et attachés avec succès.", "vector_store_id": vector_store_id}
    except Exception as e:
        logging.error(f"🚨 Erreur lors du processus d'upload et d'attachement des fichiers : {e}")
        raise RuntimeError(f"Erreur lors du processus d'upload et d'attachement des fichiers : {e}")
