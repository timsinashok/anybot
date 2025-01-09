// src/App.js
import React from 'react';
import MainLayout from './layouts/MainLayout';
import CreateView from './views/CreateView';
import EditView from './views/EditView';
import ChatView from './views/ChatView';
import { AppProvider, useAppContext } from './context/AppContext';
import './App.css';

const AppContent = () => {
  const { activeView } = useAppContext();

  const views = {
    create: <CreateView />,
    edit: <EditView />,
    chat: <ChatView />,
  };

  return <MainLayout>{views[activeView]}</MainLayout>;
};

function App() {
  return (
    <AppProvider>
      <AppContent />
    </AppProvider>
  );
}

export default App;
