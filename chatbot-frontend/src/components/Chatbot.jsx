import React, { useState } from 'react';
import { Card, Form, Button, Spinner } from 'react-bootstrap';
import { Send, Bot, ArrowLeft } from 'lucide-react';
import axios from 'axios';
import './Chatbot.css';

const Chatbot = ({ bot, onBack }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = {
      text: input,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.post('http://127.0.0.1:5000/api/chat', {
        botId: bot.id,
        query: input
      });
      
      const botMessage = {
        text: response.data.response,
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error:', error);
      const errorMessage = {
        text: 'Sorry, I encountered an error. Please try again.',
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-interface">
      <div className="chat-header bg-white p-3 rounded-3 shadow-sm mb-4">
        <div className="d-flex align-items-center">
          <Button 
            variant="light" 
            onClick={onBack}
            className="me-3 d-flex align-items-center"
            size="sm"
          >
            <ArrowLeft size={18} />
          </Button>
          <div className="bot-avatar me-3">
            <Bot size={24} />
          </div>
          <div>
            <h5 className="mb-0">{bot.name}</h5>
            <small className="text-muted">AI Assistant</small>
          </div>
        </div>
      </div>

      <Card className="chat-container shadow-sm border-0">
        <Card.Body className="chat-messages">
          {messages.length === 0 && (
            <div className="text-center text-muted my-5">
              <div className="welcome-icon mb-3">
                <Bot size={48} />
              </div>
              <h4 className="mb-2">Welcome to {bot.name}!</h4>
              <p className="text-muted">
                I'm here to help you with your questions. Feel free to ask anything!
              </p>
            </div>
          )}
          
          {messages.map((message, index) => (
            <div
              key={index}
              className={`message ${message.sender} mb-3`}
            >
              <div className="message-content">
                <div className="message-text">{message.text}</div>
                <small className="message-time">{message.timestamp}</small>
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="message bot mb-3">
              <div className="message-content d-flex align-items-center">
                <Spinner size="sm" className="me-2" animation="border" />
                Thinking...
              </div>
            </div>
          )}
        </Card.Body>

        <Card.Footer className="bg-white border-top p-3">
          <Form onSubmit={handleSubmit} className="d-flex gap-2">
            <Form.Control
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              disabled={isLoading}
              className="py-2"
            />
            <Button 
              type="submit" 
              disabled={isLoading}
              className="px-4"
            >
              <Send size={20} />
            </Button>
          </Form>
        </Card.Footer>
      </Card>
    </div>
  );
};

export default Chatbot;
