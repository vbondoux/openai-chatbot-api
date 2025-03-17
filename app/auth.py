from fastapi import APIRouter, HTTPException
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
from starlette.responses import RedirectResponse
from app.config import (
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_REDIRECT_URI
)

router = APIRouter()

# Vérification si Google OAuth est bien configuré
if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
    raise ValueError("❌ Google OAuth non configuré correctement ! Vérifie GOOGLE_SERVICE_ACCOUNT_AUTH_JSON.")

# ✅ Nouvelle configuration OAuth avec `server_metadata_url`
oauth = OAuth()
oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",  # 🔥 Charge automatiquement toutes les URLs Google
    client_kwargs={
        "scope": "openid email profile",
        "prompt": "consent",  # 🔹 Force l'affichage de l'autorisation Google
    }
)

# Route pour lancer l’authentification Google
@router.get("/login")
async def login(request: Request):
    return await oauth.google.authorize_redirect(request, GOOGLE_REDIRECT_URI)

# Callback après connexion Google
@router.get("/callback")
async def auth_callback(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = await oauth.google.parse_id_token(request, token)

        # ✅ Redirection vers le frontend après authentification réussie
        frontend_url = "https://openai-chatbot-ui-production.up.railway.app/auth-success"
        return RedirectResponse(url=f"{frontend_url}?token={token['access_token']}")

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Échec de l'authentification : {str(e)}")
