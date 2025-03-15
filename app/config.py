import os
import json
from dotenv import load_dotenv

# Charger .env en local
load_dotenv()

# Récupérer la clé API OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY non définie ! Ajoute-la dans Railway Variables ou .env.")

# Récupérer la clé API Google Drive (optionnel)
GOOGLE_DRIVE_API_KEY = os.getenv("GOOGLE_DRIVE_API_KEY")

# Récupérer le fichier JSON du compte de service
GOOGLE_SERVICE_ACCOUNT_JSON = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")

# Vérifier si Railway stocke la clé JSON sous forme de texte et recréer le fichier credentials
credentials_path = "google_credentials.json"
if GOOGLE_SERVICE_ACCOUNT_JSON and GOOGLE_SERVICE_ACCOUNT_JSON.startswith("{"):
    with open(credentials_path, "w") as f:
        f.write(GOOGLE_SERVICE_ACCOUNT_JSON)
else:
    credentials_path = GOOGLE_SERVICE_ACCOUNT_JSON  # Si c'est un chemin valide

# Exporter le bon chemin pour Google API
GOOGLE_CREDENTIALS_PATH = credentials_path

# Dossier pour stocker les fichiers téléchargés
UPLOADS_DIR = "/app/uploads"
os.makedirs(UPLOADS_DIR, exist_ok=True)

# Charger l'ID de l'assistant stocké localement
ASSISTANT_ID_FILE = "assistant_id.json"
if os.path.exists(ASSISTANT_ID_FILE):
    with open(ASSISTANT_ID_FILE, "r") as f:
        OPENAI_ASSISTANT_ID = json.load(f).get("assistant_id")
else:
    OPENAI_ASSISTANT_ID = None
