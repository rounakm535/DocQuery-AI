import google.generativeai as genai
from app.core.config import settings
from typing import List

# Configure Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)

class LLMService:
    @staticmethod
    async def generate_answer(query: str, context_chunks: List[str]) -> str:
        """
        Generate an answer to the query based on the provided context chunks using Google Gemini.
        """
        if not context_chunks:
            return "I couldn't find any relevant information in the uploaded documents to answer your question."
            
        # Combine the chunks into a single context string
        context = "\n\n---\n\n".join(context_chunks)
        
        system_instruction = (
            "You are a helpful AI assistant. Your task is to answer the user's question based ONLY on the provided document context. "
            "If the answer cannot be found in the context, clearly state that you don't know based on the provided documents. "
            "Do not use outside knowledge."
        )
        
        user_prompt = f"Context information is below:\n\n{context}\n\nQuestion: {query}\n\nAnswer:"
        
        try:
            # Initialize the model with the system instruction
            model = genai.GenerativeModel(
                model_name="gemini-flash-latest",
                system_instruction=system_instruction
            )
            
            # Generate the response
            response = await model.generate_content_async(
                user_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.1
                )
            )
            
            return response.text
        except Exception as e:
            return f"Error generating answer: {str(e)}"
