import React from 'react';

function Header() {
  return (
    <header className="header">
      <div className="logo">
        <h1>Cerebras Documentation Assistant</h1>
      </div>
      <div className="status-indicator">
        <span className="status-dot online"></span>
        <span>Online</span>
      </div>
    </header>
  );
}

export default Header;
