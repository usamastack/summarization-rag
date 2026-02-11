from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.ingestion import ingestion_service

router = APIRouter()

@router.post("/ingest", tags=["Ingestion"])
async def ingest_document(file: UploadFile = File(...)):
    try:
        content = await file.read()
        num_chunks = await ingestion_service.process_file(content, file.filename)
        return {"filename": file.filename, "chunks_processed": num_chunks, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
