import io
import PyPDF2
import docx
from fastapi import UploadFile

class DocumentProcessor:
    @staticmethod
    async def extract_text(file: UploadFile) -> str:
        """Extract text from PDF, DOCX, or TXT file."""
        content = await file.read()
        filename = file.filename.lower()
        
        text = ""
        
        if filename.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
            for page in pdf_reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
                    
        elif filename.endswith('.docx'):
            doc = docx.Document(io.BytesIO(content))
            for para in doc.paragraphs:
                text += para.text + "\n"
                
        elif filename.endswith('.txt'):
            try:
                text = content.decode('utf-8')
            except UnicodeDecodeError:
                text = content.decode('latin-1')
        else:
            raise ValueError("Unsupported file format. Please upload PDF, DOCX, or TXT.")
            
        return text.strip()

    @staticmethod
    def chunk_text(text: str, chunk_size: int = 3000, overlap: int = 300) -> list[str]:
        """Split text into smaller chunks for embedding."""
        if not text:
            return []
            
        # Basic chunking by character length
        # Using a larger chunk size to avoid hitting the 100 requests/min free tier limit.
        chunks = []
        start = 0
        text_len = len(text)
        
        while start < text_len:
            end = start + chunk_size
            
            # Try to snap to the nearest space or newline if not at the end
            if end < text_len:
                # Find the last newline or space within the chunk to avoid cutting words
                last_newline = text.rfind('\n', start, end)
                last_space = text.rfind(' ', start, end)
                
                snap_point = max(last_newline, last_space)
                if snap_point > start:
                    end = snap_point + 1
                    
            chunks.append(text[start:end].strip())
            start = end - overlap
            
        # Safeguard: if there are more than 20 chunks, we truncate to avoid exceeding the free tier 100 limit.
        if len(chunks) > 20:
            chunks = chunks[:20]
            
        return chunks
