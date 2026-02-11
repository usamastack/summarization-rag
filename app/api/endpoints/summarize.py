from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.summarizer import summarizer_service
from app.services.qdrant import qdrant_service
from app.services.embedding import embedding_service

router = APIRouter()

class SummarizeRequest(BaseModel):
    query: str = "general summary"
    strategy: str = "map_reduce"

@router.post("/summarize", tags=["Summarization"])
async def summarize_document(request: SummarizeRequest):
    try:
        # 1. Retrieve relevant chunks (RAG part)
        # If query is generic, we might want to just grab random or sequential chunks
        # But for RAG, let's use the query to find "relevant" parts to summarize
        query_vector = embedding_service.get_embedding(request.query)
        search_result = qdrant_service.search(query_vector, top_k=5)
        
        relevant_texts = [hit.payload["text"] for hit in search_result]

        # 2. Generate Summary
        summary = summarizer_service.summarize(relevant_texts, strategy=request.strategy)
        
        return {
            "query": request.query,
            "strategy": request.strategy,
            "summary": summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
