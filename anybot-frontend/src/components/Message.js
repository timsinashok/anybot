import React, { useState } from 'react';

function Message({ message }) {
  const [showSources, setShowSources] = useState(false);
  
  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className={`message ${message.type} ${message.isError ? 'error' : ''}`}>
      <div className="message-content">
        <div className="message-header">
          <span className="message-sender">{message.type === 'user' ? 'You' : 'Cerebras Assistant'}</span>
          <span className="message-time">{formatTime(message.timestamp)}</span>
        </div>
        <div className="message-text">{message.content}</div>
        
        {message.sources && message.sources.length > 0 && (
          <div className="message-sources">
            <button 
              className="sources-toggle" 
              onClick={() => setShowSources(!showSources)}
            >
              {showSources ? 'Hide Sources' : 'Show Sources'} ({message.sources.length})
            </button>
            
            {showSources && (
              <div className="sources-content">
                {message.sources.map((source, index) => (
                  <div key={index} className="source-item">
                    <div className="source-number">{index + 1}</div>
                    <div className="source-text">{source}</div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default Message;
