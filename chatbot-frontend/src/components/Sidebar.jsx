import React from 'react';
import { Nav } from 'react-bootstrap';
import { Plus, Edit, MessageSquare } from 'lucide-react';
import { useAppContext } from '../context/AppContext';

const Sidebar = () => {
  const { activeView, setActiveView } = useAppContext();

  const navItems = [
    { id: 'create', icon: Plus, label: 'Create Assistant' },
    { id: 'edit', icon: Edit, label: 'Update Assistant' },
    { id: 'chat', icon: MessageSquare, label: 'Chat Interface' },
  ];

  return (
    <div className="sidebar">
      <Nav className="flex-column">
        {navItems.map(({ id, icon: Icon, label }) => (
          <Nav.Link 
            key={id}
            className={`sidebar-link ${activeView === id ? 'active' : ''}`}
            onClick={() => setActiveView(id)}
          >
            <Icon size={20} />
            <span>{label}</span>
          </Nav.Link>
        ))}
      </Nav>
    </div>
  );
};

export default Sidebar; 