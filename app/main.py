from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from dotenv import load_dotenv
from app.api.endpoints import ingest, summarize

load_dotenv()

app = FastAPI(
    title="Summarization RAG API",
    description="High-performance Summarization API with Qdrant & Observability",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(ingest.router, prefix="/api/v1")
app.include_router(summarize.router, prefix="/api/v1")

# Instrument Prometheus
Instrumentator().instrument(app).expose(app)

@app.get("/")
async def root():
    return {"message": "Summarization RAG API is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
