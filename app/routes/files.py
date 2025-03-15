from fastapi import APIRouter, HTTPException
from app.utils.google_drive import download_drive_file

router = APIRouter()

@router.post("/download_drive_file/")
def download_google_drive_file(file_id: str):
    """
    Télécharge un fichier depuis Google Drive et retourne le chemin du fichier téléchargé.
    """
    try:
        output_path = f"/tmp/{file_id}.pdf"  # Modifier l'extension si besoin
        download_drive_file(file_id, output_path)
        return {"message": "Fichier téléchargé avec succès", "file_path": output_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
