from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.routes import agent, files, chat
from app.auth import router as auth_router

app = FastAPI(title="OpenAI Chatbot API")

# ✅ Ajouter le middleware de session (obligatoire pour OAuth)
app.add_middleware(SessionMiddleware, secret_key="CHANGE_ME_SECRET_KEY")

# Inclure les routes API existantes
app.include_router(agent.router, prefix="/agent", tags=["Agent"])
app.include_router(files.router, prefix="/files", tags=["Files"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API OpenAI Chatbot"}

# Lancer l'API avec Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
