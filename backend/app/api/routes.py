from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List

from app.services.document import DocumentProcessor
from app.services.embeddings import EmbeddingsService
from app.services.vector_store import vector_store
from app.services.llm import LLMService

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a document, extract text, embed, and store in FAISS."""
    try:
        # Clear existing knowledge base before adding new document to ensure a fresh session
        vector_store.clear()
        
        # Extract text based on file type
        text = await DocumentProcessor.extract_text(file)
        
        if not text:
            raise HTTPException(status_code=400, detail="Could not extract text from document. Document might be empty or invalid.")
            
        # Split text into chunks
        chunks = DocumentProcessor.chunk_text(text)
        
        if not chunks:
            raise HTTPException(status_code=400, detail="Document yielded no text chunks.")
            
        # Generate embeddings
        embeddings = await EmbeddingsService.get_embeddings(chunks)
        
        # Store in vector DB
        vector_store.add_texts(chunks, embeddings)
        
        return {"message": f"Successfully processed {file.filename}", "chunks_stored": len(chunks)}
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/query", response_model=QueryResponse)
async def query_document(request: QueryRequest):
    """Query the uploaded documents."""
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
        
    try:
        # Generate embedding for the question
        query_embedding_array = await EmbeddingsService.get_embeddings([question])
        
        if len(query_embedding_array) == 0:
            raise HTTPException(status_code=500, detail="Failed to generate embedding for the question.")
            
        query_embedding = query_embedding_array[0]
        
        # Search vector store for relevant chunks
        relevant_chunks = vector_store.search(query_embedding, top_k=5)
        
        # Generate answer using LLM
        answer = await LLMService.generate_answer(question, relevant_chunks)
        
        return QueryResponse(
            answer=answer,
            sources=relevant_chunks
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@router.get("/health")
def health_check():
    """Check API health and vector store status."""
    return {
        "status": "ok", 
        "vector_store_documents": vector_store.index.ntotal if vector_store.index else 0
    }

@router.post("/clear")
def clear_documents():
    """Clear all stored documents from the vector store."""
    vector_store.clear()
    return {"message": "Vector store cleared."}
