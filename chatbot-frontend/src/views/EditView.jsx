import React from 'react';
import BotEditor from '../components/BotEditor';
import { useAppContext } from '../context/AppContext';

const EditView = () => {
  const { activeBots, handleBotUpdated, setActiveBot } = useAppContext();

  return (
    <div className="edit-content">
      <h2 className="mb-4">Update Assistant</h2>
      <BotEditor 
        bots={activeBots} 
        onBotUpdated={handleBotUpdated}
        onSelectBot={setActiveBot} 
      />
    </div>
  );
};

export default EditView; 