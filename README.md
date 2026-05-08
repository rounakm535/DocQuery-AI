<div align="center">
  <h1>✨ DocQuery AI</h1>
  <p><strong>A fully free-to-deploy, AI-powered Document Question Answering System.</strong></p>

  [![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
  [![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
  [![Vite](https://img.shields.io/badge/Vite-B73BFE?style=for-the-badge&logo=vite&logoColor=FFD62E)](https://vitejs.dev/)
  [![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
</div>

<br />

DocQuery AI allows you to upload any document (PDF, DOCX, TXT) and instantly start chatting with it. Built with a hyper-modern **Glassmorphic** design, the entire stack relies entirely on free cloud tiers (Render & Vercel) and local vector storage (FAISS) so you don't spend a single cent on hosting or API credits.

---

## 🚀 Key Features

- **📄 Universal Uploads**: Seamlessly extracts text from PDFs, Word Documents, and Plain Text files.
- **🧠 Advanced RAG**: Uses **Google Gemini** embeddings (`gemini-embedding-2`) to intelligently retrieve document chunks.
- **⚡ Blazing Fast AI**: Powered by `gemini-flash-latest` for near-instant, highly accurate conversational answers.
- **🗃️ 100% Free Vector Database**: Built using Facebook's **FAISS** running locally in the backend—no need for expensive Pinecone or cloud database subscriptions.
- **🎨 Stunning UI**: Features a highly polished, responsive interface with animated mesh gradients, real-time typing indicators, and beautiful dark-mode glassmorphism.
- **🔍 Transparency**: View exactly which source chunks the AI used to generate its answers with the click of a button.

---


## 💻 Local Development Setup

If you want to run or modify this project on your local machine:

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/DocQuery-AI.git
cd DocQuery-AI
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```
Create a `.env` file inside the `backend` folder and add your API key:
```env
GEMINI_API_KEY=your_google_ai_studio_key_here
```
Run the FastAPI server:
```bash
python -m uvicorn app.main:app --reload
```

### 3. Frontend Setup
Open a new terminal window:
```bash
cd frontend
npm install
npm run dev
```
Navigate to `http://localhost:5173` in your browser and enjoy!

---
<div align="center">
 
</div>
