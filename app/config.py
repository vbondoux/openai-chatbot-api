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
if GOOGLE_SERVICE_ACCOUNT_JSON and GOOGLE_SERVICE_ACCOUNT_JSON.startswith("{"):
    credentials_path = "google_credentials.json"
    with open(credentials_path, "w") as f:
        f.write(GOOGLE_SERVICE_ACCOUNT_JSON)
else:
    credentials_path = GOOGLE_SERVICE_ACCOUNT_JSON  # Si c'est un chemin valide

# Exporter le bon chemin pour Google API
GOOGLE_CREDENTIALS_PATH = credentials_path
