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

# 🔹 🔥 AJOUT : Google OAuth 2.0 pour l'authentification WebChat 🔥
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

# ✅ On force l'URL correcte de redirection OAuth pour éviter l’erreur
GOOGLE_REDIRECT_URI = "https://openai-chatbot-api-production.up.railway.app/auth/callback"

# ✅ On utilise les URL officielles de Google pour éviter "jwks_uri missing"
GOOGLE_AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URI = "https://oauth2.googleapis.com/token"
GOOGLE_METADATA_URL = "https://accounts.google.com/.well-known/openid-configuration"
