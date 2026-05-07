import faiss
import numpy as np
import json
import os
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

# Directory to store local FAISS index and chunk mappings
STORAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "storage")
os.makedirs(STORAGE_DIR, exist_ok=True)

INDEX_PATH = os.path.join(STORAGE_DIR, "vector_index.faiss")
MAPPING_PATH = os.path.join(STORAGE_DIR, "chunk_mapping.json")

class VectorStore:
    def __init__(self, dimension: int = 3072):
        self.dimension = dimension # 3072 is the dimension for gemini-embedding-2
        self.index = None
        self.chunk_mapping: Dict[int, str] = {}
        self._load_or_create_index()
        
    def _load_or_create_index(self):
        """Load existing index from disk or create a new one."""
        if os.path.exists(INDEX_PATH) and os.path.exists(MAPPING_PATH):
            try:
                self.index = faiss.read_index(INDEX_PATH)
                with open(MAPPING_PATH, 'r') as f:
                    # JSON keys are always strings, need to convert to int
                    str_mapping = json.load(f)
                    self.chunk_mapping = {int(k): v for k, v in str_mapping.items()}
                logger.info("Loaded existing FAISS index from disk.")
            except Exception as e:
                logger.error(f"Error loading index: {e}. Creating new one.")
                self._create_new_index()
        else:
            self._create_new_index()
            
    def _create_new_index(self):
        """Create a new empty L2 index."""
        # Using IndexFlatL2 for exact search, simple and effective for small to medium docs
        self.index = faiss.IndexFlatL2(self.dimension)
        self.chunk_mapping = {}
        logger.info("Created new FAISS index.")
        
    def save(self):
        """Save index and mapping to disk."""
        faiss.write_index(self.index, INDEX_PATH)
        with open(MAPPING_PATH, 'w') as f:
            json.dump(self.chunk_mapping, f)
            
    def add_texts(self, texts: List[str], embeddings: np.ndarray):
        """Add text chunks and their embeddings to the store."""
        if len(texts) == 0 or embeddings.shape[0] == 0:
            return
            
        start_id = len(self.chunk_mapping)
        self.index.add(embeddings)
        
        for i, text in enumerate(texts):
            self.chunk_mapping[start_id + i] = text
            
        self.save()
        logger.info(f"Added {len(texts)} chunks to the vector store. Total: {self.index.ntotal}")
        
    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[str]:
        """Search for the most similar chunks given a query embedding."""
        if self.index.ntotal == 0:
            return []
            
        # Reshape query embedding if it's 1D
        if len(query_embedding.shape) == 1:
            query_embedding = query_embedding.reshape(1, -1)
            
        # Search
        distances, indices = self.index.search(query_embedding, min(top_k, self.index.ntotal))
        
        results = []
        for idx in indices[0]:
            if idx != -1 and idx in self.chunk_mapping:
                results.append(self.chunk_mapping[idx])
                
        return results
        
    def clear(self):
        """Clear the vector store."""
        self._create_new_index()
        self.save()
        
# Singleton instance
vector_store = VectorStore()
