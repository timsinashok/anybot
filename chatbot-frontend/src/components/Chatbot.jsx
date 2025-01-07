// // src/components/Homepage.js
// import React, { useState } from 'react';
// import axios from 'axios';
// import { Card, CardContent, Typography, CircularProgress, TextField, Button, Avatar } from '@mui/material';
// import { Send } from 'lucide-react';

// const Homepage = () => {
//   const [messages, setMessages] = useState([]);
//   const [input, setInput] = useState('');
//   const [isLoading, setIsLoading] = useState(false);

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     if (!input.trim()) return;

//     const userMessage = {
//       text: input,
//       sender: 'user',
//       timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
//     };

//     setMessages(prev => [...prev, userMessage]);
//     setInput('');
//     setIsLoading(true);

//     try {
//       const response = await axios.post('http://localhost:5000/api/chat', { query: input });
//       const botMessage = {
//         text: response.data.response,
//         sender: 'bot',
//         timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
//       };

//       setMessages(prev => [...prev, botMessage]);
//     } catch (error) {
//       console.error('Error:', error);
//       const errorMessage = {
//         text: 'Sorry, I encountered an error. Please try again.',
//         sender: 'bot',
//         timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
//       };
//       setMessages(prev => [...prev, errorMessage]);
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   return (
//     <div className="flex items-center justify-center min-h-screen p-4 bg-gray-100">
//       <Card className="w-full max-w-md mx-auto h-[600px] flex flex-col shadow-md">
//         <CardContent className="flex-1 overflow-y-auto p-4 flex flex-col gap-4">
//           {messages.length === 0 && (
//             <Typography variant="body1" className="text-center text-gray-500 mt-8">
//               👋 Hi! I'm here to help you with Crustdata's APIs. Ask me anything!
//             </Typography>
//           )}
//           {messages.map((message, index) => (
//             <div
//               key={index}
//               className={`flex items-start ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
//             >
//               <Avatar
//                 src={message.sender === 'user' ? '/path/to/user/avatar.jpg' : '/path/to/bot/avatar.jpg'}
//                 className={`${message.sender === 'user' ? 'order-2 ml-2' : 'order-1 mr-2'}`}
//               />
//               <div
//                 className={`max-w-[80%] p-3 rounded-lg ${
//                   message.sender === 'user'
//                     ? 'bg-blue-500 text-white order-1'
//                     : 'bg-gray-100 order-2'
//                 }`}
//               >
//                 <Typography variant="body1" className="whitespace-pre-wrap font-sans">
//                   {message.text}
//                 </Typography>
//                 <Typography variant="caption" className="text-right mt-1 block">
//                   {message.timestamp}
//                 </Typography>
//               </div>
//             </div>
//           ))}
//           {isLoading && (
//             <div className="flex justify-start">
//               <div className="bg-gray-100 p-3 rounded-lg flex items-center">
//                 <CircularProgress size={20} />
//                 <Typography variant="body1" className="ml-2">Thinking...</Typography>
//               </div>
//             </div>
//           )}
//         </CardContent>
//         <div className="p-4 border-t">
//           <form onSubmit={handleSubmit} className="flex gap-2">
//             <TextField
//               value={input}
//               onChange={(e) => setInput(e.target.value)}
//               placeholder="Ask about Crustdata's APIs..."
//               className="flex-1"
//               disabled={isLoading}
//               fullWidth
//             />
//             <Button type="submit" disabled={isLoading}>
//               <Send />
//             </Button>
//           </form>
//         </div>
//       </Card>
//     </div>
//   );
// };

// export default Homepage;


// src/components/Homepage.js
import React, { useState } from 'react';
import axios from 'axios';
import { Card, CardContent, Typography, CircularProgress, TextField, Button, Avatar } from '@mui/material';
import { Send } from 'lucide-react';
import './Homepage.css';

const Homepage = () => {
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
      const response = await axios.post('http://localhost:5000/api/chat', { query: input });
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
    <div className="homepage">
      <Card className="chat-container">
        <CardContent className="chat-window">
          {messages.length === 0 && (
            <Typography variant="body1" className="text-center text-gray-500 mt-8">
              👋 Hi! I'm here to help you with Crustdata's APIs. Ask me anything!
            </Typography>
          )}
          {messages.map((message, index) => (
            <div
              key={index}
              className={`message ${message.sender === 'user' ? 'user' : 'ai'}`}
            >
              <Avatar
                src={message.sender === 'user' ? '/path/to/user/avatar.jpg' : '/path/to/bot/avatar.jpg'}
                className={`avatar ${message.sender === 'user' ? 'user' : 'ai'}`}
              />
              <div className={`message-content ${message.sender === 'user' ? 'user' : 'ai'}`}>
                <Typography variant="body1" className="whitespace-pre-wrap font-sans">
                  {message.text}
                </Typography>
                <Typography variant="caption" className="text-right mt-1 block">
                  {message.timestamp}
                </Typography>
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="loading-message">
              <CircularProgress size={20} />
              <Typography variant="body1" className="ml-2">Thinking...</Typography>
            </div>
          )}
        </CardContent>
        <div className="chat-input">
          <form onSubmit={handleSubmit} className="input-form">
            <TextField
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about Crustdata's APIs..."
              className="input-field"
              disabled={isLoading}
              fullWidth
            />
            <Button type="submit" disabled={isLoading}>
              <Send />
            </Button>
          </form>
        </div>
      </Card>
    </div>
  );
};

export default Homepage;
