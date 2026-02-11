import io
from pypdf import PdfReader
from app.services.embedding import embedding_service
from app.services.qdrant import qdrant_service
from qdrant_client.http.models import PointStruct
import uuid

class IngestionService:
    def chunk_text(self, text, chunk_size=2000):
        # Simple splitting for summarization (larger chunks usually better)
        return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    async def process_file(self, file_content: bytes, filename: str):
        # Extract
        text = ""
        if filename.endswith(".pdf"):
            reader = PdfReader(io.BytesIO(file_content))
            for page in reader.pages:
                text += page.extract_text() + "\n"
        else:
            text = file_content.decode("utf-8")

        # Chunk
        chunks = self.chunk_text(text)

        # Embed & Upsert
        points = []
        for i, chunk in enumerate(chunks):
            vector = embedding_service.get_embedding(chunk)
            points.append(PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={"text": chunk, "filename": filename, "chunk_index": i}
            ))
        
        qdrant_service.upsert(points)
        return len(chunks)

ingestion_service = IngestionService()
