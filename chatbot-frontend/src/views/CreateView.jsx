import React from 'react';
import BotCreator from '../components/BotCreator';
import { useAppContext } from '../context/AppContext';

const CreateView = () => {
  const { handleBotCreated } = useAppContext();

  return (
    <div className="create-content">
      <h2 className="mb-4">Create New Assistant</h2>
      <BotCreator onBotCreated={handleBotCreated} />
    </div>
  );
};

export default CreateView; 