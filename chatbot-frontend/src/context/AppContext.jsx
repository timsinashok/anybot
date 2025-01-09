import React, { createContext, useContext, useState } from 'react';

const AppContext = createContext();

export const AppProvider = ({ children }) => {
  const [activeBot, setActiveBot] = useState(null);
  const [activeBots, setActiveBots] = useState([]);
  const [activeView, setActiveView] = useState('create');

  const handleBotCreated = (bot) => {
    setActiveBots([...activeBots, bot]);
    setActiveBot(bot);
    setActiveView('chat');
  };

  const handleBotUpdated = (updatedBot) => {
    const updatedBots = activeBots.map(bot => 
      bot.id === updatedBot.id ? updatedBot : bot
    );
    setActiveBots(updatedBots);
    setActiveBot(updatedBot);
    setActiveView('chat');
  };

  const value = {
    activeBot,
    setActiveBot,
    activeBots,
    setActiveBots,
    activeView,
    setActiveView,
    handleBotCreated,
    handleBotUpdated,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};

export const useAppContext = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
}; 