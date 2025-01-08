// src/App.js
import React, { useState } from 'react';
import BotCreator from './components/BotCreator';
import Chatbot from './components/Chatbot';
import { Container, Row, Col, Navbar } from 'react-bootstrap';
import { Bot } from 'lucide-react';

function App() {
  const [activeBot, setActiveBot] = useState(null);

  const handleBotCreated = (bot) => {
    setActiveBot(bot);
  };

  return (
    <div className="min-vh-100 bg-light">
      <Navbar bg="dark" variant="dark" className="mb-4">
        <Container>
          <Navbar.Brand className="d-flex align-items-center">
            <Bot size={24} className="me-2" />
            AnyBot
          </Navbar.Brand>
        </Container>
      </Navbar>

      <Container>
        <Row className="justify-content-center">
          <Col md={10} lg={8}>
            <div className="text-center mb-5">
              <h1 className="display-4 mb-3">Create Your Custom AI Assistant</h1>
              <p className="lead text-muted">
                Transform your documentation into an intelligent chatbot in minutes
              </p>
            </div>

            {activeBot ? (
              <Chatbot bot={activeBot} onBack={() => setActiveBot(null)} />
            ) : (
              <BotCreator onBotCreated={handleBotCreated} />
            )}
          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default App;
