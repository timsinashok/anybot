import React from 'react';
import { Container, Navbar, Nav, Button } from 'react-bootstrap';
import { Bot, Github } from 'lucide-react';
import Sidebar from '../components/Sidebar';

const MainLayout = ({ children }) => {
  return (
    <div className="app-wrapper">
      <Navbar bg="white" className="navbar-custom py-3 border-bottom">
        <Container fluid>
          <Navbar.Brand className="d-flex align-items-center">
            <div className="brand-logo me-2">
              <Bot size={28} />
            </div>
            <span className="brand-text">AnyBot</span>
          </Navbar.Brand>
          <Nav className="ms-auto">
            <Button 
              variant="outline-dark" 
              size="sm"
              href="https://github.com/yourusername/anybot"
              target="_blank"
              className="d-flex align-items-center gap-2"
            >
              <Github size={18} />
              <span className="d-none d-md-inline">View on GitHub</span>
            </Button>
          </Nav>
        </Container>
      </Navbar>

      <div className="d-flex flex-grow-1">
        <Sidebar />
        <main className="app-main">
          <Container fluid className="py-4">
            {children}
          </Container>
        </main>
      </div>
    </div>
  );
};

export default MainLayout; 