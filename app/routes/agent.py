from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_agent():
    return {"message": "Gestion de l'agent OpenAI"}
