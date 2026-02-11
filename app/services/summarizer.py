from openai import OpenAI
import os

class SummarizerService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def summarize(self, text_chunks: list[str], strategy: str = "map_reduce") -> str:
        if strategy == "refine":
            return self._refine_summary(text_chunks)
        else:
            return self._map_reduce_summary(text_chunks)

    def _map_reduce_summary(self, chunks: list[str]) -> str:
        # Map Step: Summarize each chunk
        chunk_summaries = []
        for chunk in chunks:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                    {"role": "user", "content": f"Summarize the following text concisely:\n\n{chunk}"}
                ]
            )
            chunk_summaries.append(response.choices[0].message.content)

        # Reduce Step: Summarize the summaries
        combined_text = "\n\n".join(chunk_summaries)
        final_response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are an expert summarizer. Synthesize the following points into a coherent, detailed summary."},
                {"role": "user", "content": f"Points:\n{combined_text}"}
            ]
        )
        return final_response.choices[0].message.content

    def _refine_summary(self, chunks: list[str]) -> str:
        existing_summary = ""
        for i, chunk in enumerate(chunks):
            if i == 0:
                prompt = f"Summarize the following text:\n\n{chunk}"
            else:
                prompt = f"Here is the existing summary:\n{existing_summary}\n\nWe have the opportunity to refine the existing summary (only if needed) with some more context below.\n------------\n{chunk}\n------------\nGiven the new context, refine the original summary. If the context isn't useful, return the original summary."

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo", # Cheaper for iterative
                messages=[{"role": "user", "content": prompt}]
            )
            existing_summary = response.choices[0].message.content
        
        return existing_summary

summarizer_service = SummarizerService()
