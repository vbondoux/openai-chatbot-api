from fastapi import FastAPI
from app.routes import agent, files, chat

app = FastAPI(title="OpenAI Chatbot API")

# Inclure les routes (vont être définies dans les fichiers correspondants)
app.include_router(agent.router, prefix="/agent", tags=["Agent"])
app.include_router(files.router, prefix="/files", tags=["Files"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API OpenAI Chatbot"}

# Lancer l'API avec Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
