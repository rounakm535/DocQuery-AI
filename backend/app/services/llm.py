import os
from openai import OpenAI
from app.core.config import settings
from typing import List
import logging

logger = logging.getLogger(__name__)

class LLMService:
    @staticmethod
    async def generate_answer(query: str, context_chunks: List[str]) -> str:
        """
        Generate an answer to the query based on the provided context chunks using xAI's Grok.
        """
        if not context_chunks:
            return "I couldn't find any relevant information in the uploaded documents to answer your question."
            
        if not settings.XAI_API_KEY or settings.XAI_API_KEY == "your_xai_api_key_here":
            return "Error: XAI_API_KEY is not configured. Please generate an API key from console.x.ai and add it to your .env file."
            
        # Combine the chunks into a single context string
        context = "\n\n---\n\n".join(context_chunks)
        
        system_instruction = (
            "You are Grok, an AI trained by xAI. Your task is to answer the user's question based ONLY on the provided document context. "
            "If the answer cannot be found in the context, clearly state that you don't know based on the provided documents. "
            "Do not use outside knowledge."
        )
        
        user_prompt = f"Context information is below:\n\n{context}\n\nQuestion: {query}\n\nAnswer:"
        
        try:
            client = OpenAI(
                api_key=settings.XAI_API_KEY,
                base_url="https://api.x.ai/v1"
            )
            
            # Note: We're using the sync client here in an async wrapper, but for small payloads this is generally fine.
            # Grok supports standard chat completions format.
            response = client.chat.completions.create(
                model="grok-beta",
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating answer with Grok: {str(e)}")
            return f"Error generating answer: {str(e)}"
