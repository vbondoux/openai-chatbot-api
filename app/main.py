from fastapi import FastAPI

app = FastAPI(title="OpenAI Chatbot API")

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API OpenAI Chatbot"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
