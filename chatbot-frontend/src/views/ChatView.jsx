import React from 'react';
import {
  Box,
  Typography,
  Card,
  Button,
  Grid,
  Chip,
  useTheme,
} from '@mui/material';
import { Add as AddIcon, Chat as ChatIcon } from '@mui/icons-material';
import Chatbot from '../components/Chatbot';
import { motion } from 'framer-motion';
import { useAppContext } from '../context/AppContext';

const ChatView = () => {
  const theme = useTheme();
  const { activeBot, setActiveBot, setActiveView, activeBots } = useAppContext();

  if (!activeBot) {
    return (
      <Box>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <Typography 
            variant="h1" 
            sx={{ 
              fontSize: { xs: '2rem', md: '2.5rem' },
              mb: 2,
              background: `linear-gradient(120deg, ${theme.palette.primary.main}, ${theme.palette.primary.light})`,
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
            }}
          >
            AI Assistants
          </Typography>
          <Typography 
            variant="subtitle1" 
            color="text.secondary"
            sx={{ mb: 4, maxWidth: 600 }}
          >
            Select an existing assistant to start chatting or create a new one.
          </Typography>
        </motion.div>

        <Grid container spacing={3}>
          {activeBots.length > 0 ? (
            activeBots.map((bot, index) => (
              <Grid item xs={12} sm={6} md={4} key={bot.id}>
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                >
                  <Card 
                    sx={{ 
                      p: 3,
                      cursor: 'pointer',
                      transition: 'all 0.2s',
                      '&:hover': {
                        transform: 'translateY(-4px)',
                        boxShadow: theme.shadows[4],
                      },
                    }}
                    onClick={() => setActiveBot(bot)}
                  >
                    <Box sx={{ mb: 2 }}>
                      <ChatIcon 
                        sx={{ 
                          fontSize: 40,
                          color: theme.palette.primary.main,
                        }} 
                      />
                    </Box>
                    <Typography variant="h6" gutterBottom>
                      {bot.name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                      Trained on {bot.documents?.length || 0} documents
                    </Typography>
                    <Chip 
                      label="Active" 
                      size="small"
                      sx={{ 
                        bgcolor: 'success.light',
                        color: 'success.dark',
                      }} 
                    />
                  </Card>
                </motion.div>
              </Grid>
            ))
          ) : (
            <Grid item xs={12}>
              <Card sx={{ p: 4, textAlign: 'center' }}>
                <Box sx={{ mb: 3 }}>
                  <ChatIcon sx={{ fontSize: 60, color: 'text.secondary', opacity: 0.5 }} />
                </Box>
                <Typography variant="h6" gutterBottom>
                  No Assistants Available
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                  Create your first AI assistant to get started
                </Typography>
                <Button
                  variant="contained"
                  startIcon={<AddIcon />}
                  onClick={() => setActiveView('create')}
                >
                  Create Assistant
                </Button>
              </Card>
            </Grid>
          )}
        </Grid>
      </Box>
    );
  }

  return (
    <Box>
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
      >
        <Card 
          sx={{ 
            height: 'calc(100vh - 180px)',
            display: 'flex',
            flexDirection: 'column',
            overflow: 'hidden',
          }}
        >
          <Chatbot bot={activeBot} />
        </Card>
      </motion.div>
    </Box>
  );
};

export default ChatView; 