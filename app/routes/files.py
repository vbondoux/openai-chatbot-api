from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_files():
    return {"message": "Gestion des fichiers"}
