import ollama
from app.core.config import settings
from app.utils.logging_config import logger

class GenerationService:
    def build_prompt(self, query: str, context_chunks: list[dict]) -> str:
        context_sections = []
        for idx, item in enumerate(context_chunks, start=1):
            context_sections.append(
                f"[Doc {idx}] Source: {item['source']} (Page {item['page']})\n"
                f"Content: {item['text']}"
            )
        formatted_context = "\n\n".join(context_sections)

        prompt = f"""You are an HR Assistant. Answer the question based on the provided document excerpts.

Context:
{formatted_context}

Question: {query}

Instructions:
- Summarize what the excerpts state regarding the question.
- Cite the source document and page number for each point (e.g., [Source: <file>, Page <num>]).
- If the excerpts mention nothing relevant to the question at all, respond: "I don't have enough information to answer that."

Answer:"""
        return prompt

    def generate_answer(self, query: str, context_chunks: list[dict]) -> dict:
        prompt = self.build_prompt(query, context_chunks)
        
        response = ollama.chat(
            model=settings.OLLAMA_MODEL,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.1}
        )
        
        answer_text = response["message"]["content"]
        cited_sources = sorted(list({
            f"{c['source']} (Page {c['page']})" for c in context_chunks
        }))
        
        return {
            "answer": answer_text,
            "sources": cited_sources
        }

generation_service = GenerationService()