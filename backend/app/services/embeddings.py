import numpy as np
import google.generativeai as genai
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Configure Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)

class EmbeddingsService:
    @staticmethod
    async def get_embeddings(texts: list[str]) -> np.ndarray:
        """
        Generate embeddings for a list of text chunks using Gemini API.
        Uses gemini-embedding-2.
        """
        import asyncio
        if not texts:
            return np.array([])
            
        all_embeddings = []
        batch_size = 20 # Small batches to be safe
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            
            success = False
            retries = 0
            while not success and retries < 3:
                try:
                    result = genai.embed_content(
                        model="models/gemini-embedding-2",
                        content=batch,
                        task_type="retrieval_document"
                    )
                    all_embeddings.extend(result['embedding'])
                    success = True
                except Exception as e:
                    error_str = str(e).lower()
                    if "429" in error_str or "quota" in error_str:
                        retries += 1
                        logger.warning(f"Rate limit hit. Waiting 40 seconds... (Attempt {retries}/3)")
                        await asyncio.sleep(40)
                    else:
                        logger.error(f"Error generating embeddings: {e}")
                        raise e
                        
            if not success:
                raise Exception("Exceeded rate limit retries. Please wait a minute and try again.")
                
        return np.array(all_embeddings, dtype=np.float32)
