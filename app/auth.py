from fastapi import APIRouter, HTTPException
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
from starlette.responses import RedirectResponse
from app.config import (
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_REDIRECT_URI,
    GOOGLE_AUTH_URI,
    GOOGLE_TOKEN_URI
)

router = APIRouter()

# Vérification si Google OAuth est bien configuré
if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
    raise ValueError("❌ Google OAuth non configuré correctement ! Vérifie GOOGLE_SERVICE_ACCOUNT_AUTH_JSON.")

# Configuration OAuth
oauth = OAuth()
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    authorize_url=GOOGLE_AUTH_URI,
    access_token_url=GOOGLE_TOKEN_URI,
    client_kwargs={"scope": "openid email profile"},
)

# Route pour lancer l’authentification Google
@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

# Callback après connexion Google
@router.get("/auth/callback")
async def auth_callback(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = await oauth.google.parse_id_token(request, token)

        return {
            "email": user_info["email"],
            "name": user_info.get("name", "Utilisateur"),
            "picture": user_info.get("picture", ""),
            "token": token["access_token"]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Échec de l'authentification : {str(e)}")
