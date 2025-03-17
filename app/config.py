import os
import json
from dotenv import load_dotenv

# Charger .env en local
load_dotenv()

# 🔹 Clé API OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY non définie ! Ajoute-la dans Railway Variables ou .env.")

# 🔹 Clé API Google Drive (optionnel)
GOOGLE_DRIVE_API_KEY = os.getenv("GOOGLE_DRIVE_API_KEY")

# 🔹 Récupérer le fichier JSON du compte de service (Google Drive)
GOOGLE_SERVICE_ACCOUNT_JSON = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")

# 🔹 Vérifier si Railway stocke la clé JSON sous forme de texte et recréer le fichier credentials
credentials_path = "google_credentials.json"
if GOOGLE_SERVICE_ACCOUNT_JSON and GOOGLE_SERVICE_ACCOUNT_JSON.startswith("{"):
    with open(credentials_path, "w") as f:
        f.write(GOOGLE_SERVICE_ACCOUNT_JSON)
else:
    credentials_path = GOOGLE_SERVICE_ACCOUNT_JSON  # Si c'est un chemin valide

# 🔹 Exporter le bon chemin pour Google API (Drive)
GOOGLE_CREDENTIALS_PATH = credentials_path

# 🔹 Dossier pour stocker les fichiers téléchargés
UPLOADS_DIR = "/app/uploads"
os.makedirs(UPLOADS_DIR, exist_ok=True)

GOOGLE_DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "")

# 🔹 🔥 Google OAuth 2.0 pour l'authentification WebChat 🔥
GOOGLE_AUTH_JSON = os.getenv("GOOGLE_SERVICE_ACCOUNT_AUTH_JSON")

if GOOGLE_AUTH_JSON:
    GOOGLE_AUTH_CONFIG = json.loads(GOOGLE_AUTH_JSON)

    GOOGLE_CLIENT_ID = GOOGLE_AUTH_CONFIG["web"]["client_id"]
    GOOGLE_CLIENT_SECRET = GOOGLE_AUTH_CONFIG["web"]["client_secret"]
    GOOGLE_REDIRECT_URI = GOOGLE_AUTH_CONFIG["web"]["redirect_uris"][0]
else:
    GOOGLE_CLIENT_ID = None
    GOOGLE_CLIENT_SECRET = None
    GOOGLE_REDIRECT_URI = None
    print("⚠️ GOOGLE_SERVICE_ACCOUNT_AUTH_JSON non défini !")
