# Summarization RAG with Observability 🚀

A high-performance, containerized RAG system focused on **Intelligent Summarization**. Built with **FastAPI**, **Qdrant**, and a full **Prometheus/Grafana** observability stack.

## ✨ Fancy Features

- **Advanced Summarization**: 
  - **Map-Reduce**: Handles large documents by summarizing chunks and synthesizing them.
  - **Refine**: Iteratively improves summaries with new context.
- **Vector Search**: Self-hosted **Qdrant** for lightning-fast retrieval.
- **Observability**:
  - **Prometheus**: Real-time metrics scraping.
  - **Grafana**: Beautiful dashboards for request latency, token usage, and errors.
- **Dockerized**: Entire stack spins up with one command.

## 🛠️ Stack

- **Backend**: FastAPI (Python 3.10)
- **Vector DB**: Qdrant
- **LLM**: OpenAI GPT-4 Turbo
- **Monitoring**: Prometheus + Grafana

## 🚀 Getting Started

### 1. Prerequisites
- Docker & Docker Compose
- OpenAI API Key

### 2. Environment Setup
Create a `.env` file in `summarization-rag/`:
```env
OPENAI_API_KEY=sk-your-key-here
```

### 3. Run the Stack
```bash
docker-compose up -d --build
```
This will start:
- **API**: `http://localhost:8000`
- **Qdrant**: `http://localhost:6333`
- **Prometheus**: `http://localhost:9090`
- **Grafana**: `http://localhost:3000` (User: `admin`, Pass: `admin`)

## 📊 Observability

Log in to Grafana at `http://localhost:3000`. You will see pre-configured dashboards showing:
- API Request Rate
- Latency Percentiles (p95, p99)
- Summarization Token Usage

## 🔌 API Usage

### Ingest a Document
```bash
curl -X POST "http://localhost:8000/api/v1/ingest" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your-document.pdf"
```

### Generate Summary
```bash
curl -X POST "http://localhost:8000/api/v1/summarize" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "market trends",
    "strategy": "map_reduce"
  }'
```

## 📂 Structure
```
summarization-rag/
├── app/
│   ├── api/            # Endpoints
│   ├── services/       # Logic (Qdrant, OpenAI, Summarizer)
│   └── main.py         # Entry point
├── docker/             # Configs for Prometheus/Grafana
├── docker-compose.yml  # Stack definition
└── requirements.txt
```
