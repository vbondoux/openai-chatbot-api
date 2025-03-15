import os
import json
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Clé API OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY non définie ! Ajoute-la dans Railway Variables ou .env.")

# Clé API Google Drive (optionnel)
GOOGLE_DRIVE_API_KEY = os.getenv("GOOGLE_DRIVE_API_KEY")

# Chargement des credentials du compte de service Google
GOOGLE_SERVICE_ACCOUNT_JSON = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
if GOOGLE_SERVICE_ACCOUNT_JSON and GOOGLE_SERVICE_ACCOUNT_JSON.startswith("{"):
    with open("google_credentials.json", "w") as f:
        f.write(GOOGLE_SERVICE_ACCOUNT_JSON)
    GOOGLE_SERVICE_ACCOUNT_JSON = "google_credentials.json"

# Fichier pour stocker l'Assistant ID d'OpenAI
ASSISTANT_FILE = "assistant.json"

def get_assistant_id():
    """
    Récupère l'assistant_id stocké localement, ou retourne None s'il n'existe pas.
    """
    if os.path.exists(ASSISTANT_FILE):
        with open(ASSISTANT_FILE, "r") as f:
            data = json.load(f)
            return data.get("assistant_id")
    return None

def save_assistant_id(assistant_id):
    """
    Sauvegarde l'assistant_id dans un fichier JSON.
    """
    with open(ASSISTANT_FILE, "w") as f:
        json.dump({"assistant_id": assistant_id}, f)
