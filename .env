import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env si présent (utile en local)
load_dotenv()

# Récupérer la clé API depuis les variables d'environnement (Railway ou .env)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY non définie ! Ajoute-la dans Railway Variables ou .env.")
