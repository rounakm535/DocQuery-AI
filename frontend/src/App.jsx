import DocumentUpload from './components/DocumentUpload';
import ChatInterface from './components/ChatInterface';

function App() {
  return (
    <div className="app-container">
      <div className="sidebar">
        <div>
          <h1>DocQuery AI</h1>
          <p>Powered by Google Gemini & FAISS</p>
        </div>
        <DocumentUpload />
        <div style={{ marginTop: 'auto', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
          <p>Chat with Your Documents.</p>
        </div>
      </div>
      <ChatInterface />
    </div>
  );
}

export default App;
