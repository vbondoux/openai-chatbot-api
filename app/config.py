import os
from dotenv import load_dotenv

# Charger .env en local
load_dotenv()

# Récupérer la clé API (Railway ou .env)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY non définie ! Ajoute-la dans Railway Variables ou .env.")


# Récupérer la clé API Google Drive (optionnel)
GOOGLE_DRIVE_API_KEY = os.getenv("GOOGLE_DRIVE_API_KEY")

# Récupérer le fichier JSON du compte de service
GOOGLE_SERVICE_ACCOUNT_JSON = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")

# Si Railway stocke la clé JSON en tant que variable d'environnement, il faut la reconstituer
if GOOGLE_SERVICE_ACCOUNT_JSON and GOOGLE_SERVICE_ACCOUNT_JSON.startswith("{"):
    with open("google_credentials.json", "w") as f:
        f.write(GOOGLE_SERVICE_ACCOUNT_JSON)
    GOOGLE_SERVICE_ACCOUNT_JSON = "google_credentials.json"
