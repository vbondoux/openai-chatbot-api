import os
import json
from dotenv import load_dotenv

# Charger .env en local
load_dotenv()

# Clé API OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Vérifier que la clé API OpenAI est bien définie
if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY non définie ! Ajoute-la dans Railway Variables ou .env.")

# Récupérer les credentials Google Drive
GOOGLE_SERVICE_ACCOUNT_JSON = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")

# Si Railway stocke la clé JSON en tant que variable d'environnement, il faut la reconstituer
GOOGLE_CREDENTIALS_PATH = "google_credentials.json"
if GOOGLE_SERVICE_ACCOUNT_JSON and GOOGLE_SERVICE_ACCOUNT_JSON.startswith("{"):
    with open(GOOGLE_CREDENTIALS_PATH, "w") as f:
        f.write(GOOGLE_SERVICE_ACCOUNT_JSON)

# Chemin du dossier d'uploads (créé dynamiquement s'il n'existe pas)
UPLOADS_DIR = "/app/uploads"
os.makedirs(UPLOADS_DIR, exist_ok=True)

# Gestion de l'assistant OpenAI
ASSISTANT_ID_FILE = "assistant_id.json"

def save_assistant_id(assistant_id):
    """ Sauvegarde l'ID de l'assistant OpenAI. """
    with open(ASSISTANT_ID_FILE, "w") as f:
        json.dump({"assistant_id": assistant_id}, f)

def load_assistant_id():
    """ Charge l'ID de l'assistant s'il a déjà été créé. """
    if os.path.exists(ASSISTANT_ID_FILE):
        with open(ASSISTANT_ID_FILE, "r") as f:
            return json.load(f).get("assistant_id")
    return None
