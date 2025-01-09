import React from 'react';
import Chatbot from '../components/Chatbot';
import { Button } from 'react-bootstrap';
import { useAppContext } from '../context/AppContext';

const ChatView = () => {
  const { activeBot, setActiveView } = useAppContext();

  return (
    <div className="chat-content">
      <h2 className="mb-4">Chat with Assistant</h2>
      {activeBot ? (
        <Chatbot bot={activeBot} />
      ) : (
        <div className="text-center py-5">
          <p>Please select a bot to start chatting</p>
          <Button onClick={() => setActiveView('create')}>
            Create New Bot
          </Button>
        </div>
      )}
    </div>
  );
};

export default ChatView; 