import React, { useState, useRef, useEffect } from 'react';
import './App.css';
import MessageList from './components/MessageList';
import InputArea from './components/InputArea';
import Header from './components/Header';
import axios from 'axios';

function App() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Add a welcome message when the app first loads
  useEffect(() => {
    setMessages([
      {
        type: 'bot',
        content: "Welcome to Cerebras Documentation Assistant! How can I help you today?",
        timestamp: new Date()
      }
    ]);
  }, []);

  const handleSendMessage = async (message) => {
    if (!message.trim()) return;

    // Add user message to chat
    const userMessage = {
      type: 'user',
      content: message,
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setLoading(true);

    try {
      // Call the API
      const response = await axios.post('http://127.0.0.1:8000/query', {
        query: message,
        top_n: 2
      });
      // Add bot response to chat
      const botMessage = {
        type: 'bot',
        content: response.data.llm_response,
        sources: response.data.results,
        metadata: response.data.metadata,
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error:', error);
      
      // Add error message
      const errorMessage = {
        type: 'bot',
        content: "Sorry, I encountered an error while processing your request. Please try again.",
        isError: true,
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <Header />
      <div className="chat-container">
        <MessageList messages={messages} />
        <div ref={messagesEndRef} />
        <InputArea onSendMessage={handleSendMessage} loading={loading} />
      </div>
    </div>
  );
}

export default App;
