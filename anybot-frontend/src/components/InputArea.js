import React, { useState } from 'react';

function InputArea({ onSendMessage, loading }) {
  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim() && !loading) {
      onSendMessage(message);
      setMessage('');
    }
  };

  return (
    <div className="input-area">
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Ask about Cerebras documentation..."
          disabled={loading}
        />
        <button 
          type="submit" 
          disabled={loading || !message.trim()}
          className={loading ? 'loading' : ''}
        >
          {loading ? (
            <span className="loading-spinner"></span>
          ) : (
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"></path>
            </svg>
          )}
        </button>
      </form>
    </div>
  );
}

export default InputArea;
