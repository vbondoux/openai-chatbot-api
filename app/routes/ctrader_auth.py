from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, HTMLResponse
import requests
import os

router = APIRouter()

CLIENT_ID = os.getenv("CTRADER_CLIENT_ID")
CLIENT_SECRET = os.getenv("CTRADER_CLIENT_SECRET")
REDIRECT_URI = os.getenv("CTRADER_REDIRECT_URI")
TOKEN_URL = "https://connect.spotware.com/apps/token"

@router.get("/auth/ctrader")
def auth_ctrader():
    auth_url = (
        "https://connect.spotware.com/apps/authorize"
        f"?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
    )
    return RedirectResponse(auth_url)

@router.get("/auth/ctrader/callback")
def auth_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return HTMLResponse("❌ Erreur : aucun code reçu", status_code=400)

    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "code": code
    }
    response = requests.post(TOKEN_URL, data=data)

    if response.status_code == 200:
        tokens = response.json()
        return {
            "✅ Access Token": tokens["access_token"],
            "🔁 Refresh Token": tokens["refresh_token"],
            "⏱️ Expire dans (s)": tokens["expires_in"]
        }
    else:
        return HTMLResponse(f"❌ Échec : {response.text}", status_code=400)
