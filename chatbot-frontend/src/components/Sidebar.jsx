import React from 'react';
import { 
  Box, 
  List, 
  ListItem, 
  ListItemButton, 
  ListItemIcon, 
  ListItemText,
  Typography,
  Divider,
} from '@mui/material';
import { 
  Add as AddIcon,
  Edit as EditIcon,
  Chat as ChatIcon,
} from '@mui/icons-material';
import { useAppContext } from '../context/AppContext';
import { motion } from 'framer-motion';

const Sidebar = () => {
  const { activeView, setActiveView } = useAppContext();

  const menuItems = [
    { id: 'create', icon: AddIcon, label: 'Create Assistant' },
    { id: 'edit', icon: EditIcon, label: 'Update Assistant' },
    { id: 'chat', icon: ChatIcon, label: 'Chat Interface' },
  ];

  return (
    <Box sx={{ pt: { xs: 2, sm: 8 }, pb: 2 }}>
      <Box sx={{ px: 3, mb: 3 }}>
        <Typography 
          variant="overline" 
          sx={{ 
            color: 'text.secondary',
            fontWeight: 500,
          }}
        >
          Navigation
        </Typography>
      </Box>
      <List>
        {menuItems.map(({ id, icon: Icon, label }) => (
          <ListItem key={id} disablePadding>
            <ListItemButton
              selected={activeView === id}
              onClick={() => setActiveView(id)}
              sx={{
                mx: 1,
                borderRadius: 1,
                '&.Mui-selected': {
                  bgcolor: 'primary.light',
                  color: 'primary.contrastText',
                  '&:hover': {
                    bgcolor: 'primary.light',
                  },
                  '& .MuiListItemIcon-root': {
                    color: 'inherit',
                  },
                },
              }}
            >
              <ListItemIcon sx={{ minWidth: 40 }}>
                <Icon />
              </ListItemIcon>
              <ListItemText 
                primary={label}
                primaryTypographyProps={{
                  fontSize: '0.875rem',
                  fontWeight: 500,
                }}
              />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Box>
  );
};

export default Sidebar; 