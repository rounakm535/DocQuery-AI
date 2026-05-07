import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, FileText, ChevronDown, ChevronUp, Bot } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

export default function ChatInterface() {
  const [messages, setMessages] = useState(() => {
    const saved = sessionStorage.getItem('chatHistory');
    if (saved) {
      return JSON.parse(saved);
    }
    return [];
  });
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    sessionStorage.setItem('chatHistory', JSON.stringify(messages));
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;
    
    const userQuery = input.trim();
    setInput('');
    
    setMessages(prev => [...prev, { role: 'user', content: userQuery, sources: null }]);
    setIsLoading(true);
    
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await axios.post(`${apiUrl}/api/v1/query`, {
        question: userQuery
      });
      
      setMessages(prev => [...prev, { 
        role: 'bot', 
        content: response.data.answer, 
        sources: response.data.sources 
      }]);
    } catch (error) {
      console.error(error);
      setMessages(prev => [...prev, { 
        role: 'bot', 
        content: 'Sorry, I encountered an error. Is the backend running? Have you uploaded a document?', 
        sources: null 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="main-content">
      <div className="chat-container">
        {messages.length === 0 && (
          <div className="empty-state">
            <Bot className="empty-state-icon" />
            <h2>How can I help you today?</h2>
            <p>Upload a document from the sidebar to get started.</p>
          </div>
        )}
      
        {messages.map((msg, idx) => (
          <div key={idx} className={`message message-${msg.role}`}>
            <div className="message-role">
              {msg.role === 'user' ? 'You' : 'DocQuery AI'}
            </div>
            
            <div className="message-content" style={{ whiteSpace: msg.role === 'user' ? 'pre-wrap' : 'normal' }}>
              {msg.role === 'bot' ? (
                <ReactMarkdown>{msg.content}</ReactMarkdown>
              ) : (
                msg.content
              )}
            </div>
            
            {msg.sources && msg.sources.length > 0 && (
              <SourceViewer sources={msg.sources} />
            )}
          </div>
        ))}
        
        {isLoading && (
          <div className="message message-bot">
             <div className="message-role">DocQuery AI</div>
            <div className="typing-indicator">
              <span></span><span></span><span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      
      <div className="input-container">
        <div className="input-pill">
          <input 
            type="text" 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask a question about your documents..." 
            disabled={isLoading}
          />
          <button onClick={handleSend} disabled={isLoading || !input.trim()}>
            <Send size={18} />
          </button>
        </div>
      </div>
    </div>
  );
}

function SourceViewer({ sources }) {
  const [expanded, setExpanded] = useState(false);
  
  if (!sources || sources.length === 0) return null;
  
  return (
    <div className="source-chunks">
      <div 
        className="source-title" 
        onClick={() => setExpanded(!expanded)}
      >
        <FileText size={14} />
        <span>View {sources.length} Retrieved Source Chunks</span>
        {expanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
      </div>
      
      {expanded && (
        <div style={{ marginTop: '12px' }}>
          {sources.map((source, idx) => (
            <div key={idx} className="source-content">
              {source}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
