from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

router = APIRouter()

# 🔹 Authentification désactivée temporairement
@router.get("/login")
async def login(request: Request):
    return JSONResponse(
        status_code=503,
        content={"message": "L'authentification Google OAuth est désactivée temporairement."}
    )

@router.get("/callback")
async def auth_callback(request: Request):
    return JSONResponse(
        status_code=503,
        content={"message": "L'authentification Google OAuth est désactivée temporairement."}
    )
