import { useState, useRef } from 'react';
import axios from 'axios';
import { UploadCloud, CheckCircle, AlertCircle, Loader } from 'lucide-react';

export default function DocumentUpload() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState('idle'); // idle, uploading, success, error
  const [message, setMessage] = useState('');
  const [isDragActive, setIsDragActive] = useState(false);
  const fileInputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setIsDragActive(true);
    } else if (e.type === 'dragleave') {
      setIsDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelection(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelection(e.target.files[0]);
    }
  };

  const handleFileSelection = (selectedFile) => {
    const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];

    if (validTypes.includes(selectedFile.type) || selectedFile.name.match(/\.(pdf|docx|txt)$/i)) {
      setFile(selectedFile);
      uploadFile(selectedFile);
    } else {
      setStatus('error');
      setMessage('Invalid file type. Please upload PDF, DOCX, or TXT.');
    }
  };

  const uploadFile = async (fileToUpload) => {
    setStatus('uploading');
    setMessage('Extracting text and generating embeddings...');

    const formData = new FormData();
    formData.append('file', fileToUpload);

    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    try {
      const response = await axios.post(`${apiUrl}/api/v1/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setStatus('success');
      setMessage(`Successfully processed ${fileToUpload.name}.`);
    } catch (error) {
      console.error(error);
      setStatus('error');
      setMessage(error.response?.data?.detail || 'Failed to upload document. Is the backend running?');
    }
  };

  return (
    <div className="glass" style={{ padding: '24px', borderRadius: '16px' }}>
      <h2>Knowledge Base</h2>
      <p style={{ marginBottom: '16px', marginTop: '4px' }}>Upload a document to chat with it.</p>

      <div
        className={`upload-zone ${isDragActive ? 'drag-active' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          style={{ display: 'none' }}
          accept=".pdf,.docx,.txt"
        />

        {status === 'uploading' ? (
          <Loader className="upload-icon" style={{ animation: 'spin 2s linear infinite' }} />
        ) : (
          <UploadCloud className="upload-icon" />
        )}

        <div style={{ textAlign: 'center' }}>
          <p style={{ fontWeight: 500, color: 'var(--text-main)' }}>
            {status === 'uploading' ? 'Processing Document...' : 'Click or drag file to upload'}
          </p>
          <p style={{ fontSize: '0.8rem', marginTop: '4px' }}>Supports PDF, DOCX, TXT</p>
        </div>
      </div>

      {status === 'success' && (
        <div className="alert alert-success">
          <CheckCircle size={18} />
          <div>{message}</div>
        </div>
      )}

      {status === 'error' && (
        <div className="alert alert-error">
          <AlertCircle size={18} />
          <div>{message}</div>
        </div>
      )}

      {file && status !== 'uploading' && status !== 'error' && (
        <div style={{ marginTop: '16px', display: 'flex', justifyContent: 'center' }}>
          <button 
            onClick={() => { setFile(null); setStatus('idle'); }}
            style={{ background: 'transparent', border: '1px solid rgba(139, 92, 246, 0.5)', color: 'var(--primary)' }}
          >
            Upload Another
          </button>
        </div>
      )}
    </div>
  );
}
