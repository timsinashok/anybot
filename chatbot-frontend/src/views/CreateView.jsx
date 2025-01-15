import React from 'react';
import {
  Box,
  Typography,
  Card,
  Grid,
  Button,
  Divider,
  useTheme,
} from '@mui/material';
import { Add as AddIcon, ArrowForward } from '@mui/icons-material';
import BotCreator from '../components/BotCreator';
import { motion } from 'framer-motion';
import { useAppContext } from '../context/AppContext';

const CreateView = () => {
  const theme = useTheme();
  const { handleBotCreated } = useAppContext();

  return (
    <Box>
      <Box sx={{ mb: 6 }}>
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
            Create Your AI Assistant
          </Typography>
          <Typography 
            variant="subtitle1" 
            color="text.secondary"
            sx={{ maxWidth: 600 }}
          >
            Transform your documentation into an intelligent chatbot. Upload files, add URLs, 
            and let AI create a personalized assistant for your needs.
          </Typography>
        </motion.div>
      </Box>

      <Grid container spacing={4}>
        <Grid item xs={12} md={4}>
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <Card 
              sx={{ 
                p: 3,
                height: '100%',
                background: `linear-gradient(45deg, ${theme.palette.primary.dark}, ${theme.palette.primary.main})`,
                color: 'white',
              }}
            >
              <Typography variant="h6" sx={{ mb: 2 }}>
                Why Create an AI Assistant?
              </Typography>
              <Divider sx={{ borderColor: 'rgba(255,255,255,0.1)', my: 2 }} />
              <Box sx={{ mb: 3 }}>
                {[
                  '24/7 availability for your users',
                  'Instant access to documentation',
                  'Consistent and accurate responses',
                  'Reduced support workload',
                ].map((benefit, index) => (
                  <Box 
                    key={index} 
                    sx={{ 
                      display: 'flex', 
                      alignItems: 'center',
                      mb: 2,
                    }}
                  >
                    <ArrowForward sx={{ mr: 1, fontSize: 16 }} />
                    <Typography variant="body2">
                      {benefit}
                    </Typography>
                  </Box>
                ))}
              </Box>
            </Card>
          </motion.div>
        </Grid>

        <Grid item xs={12} md={8}>
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
          >
            <Card sx={{ p: 3 }}>
              <Box sx={{ mb: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Assistant Configuration
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Configure your AI assistant by providing the necessary information and documentation.
                </Typography>
              </Box>
              <BotCreator onBotCreated={handleBotCreated} />
            </Card>
          </motion.div>
        </Grid>
      </Grid>
    </Box>
  );
};

export default CreateView; 