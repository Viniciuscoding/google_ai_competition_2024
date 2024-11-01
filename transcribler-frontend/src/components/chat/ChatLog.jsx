/* eslint-disable react/prop-types */

import { useState, useEffect } from 'react';
import Grid from '@mui/material/Grid2';
import Paper from '@mui/material/Paper';

import './styles.css';

function ChatLog(props) {
  const [log, setLog] = useState([]);

  useEffect(() => {
    if (props.sendMessage) {
      console.log(props.sendMessage)
      setLog((prevLog) => [...prevLog, props.sendMessage]);
    }
  }, [props.sendMessage]);

  return (
    <Grid container direction="column" spacing={2} sx={{ textAlign: 'left' }}>
      {log.map((message, index) => (
        <Grid
          key={index}
          item
          display="flex"
          justifyContent={message.sender === 'User' ? 'flex-end' : 'flex-start'}
        >
          <Paper
            sx={{
              maxWidth: '25rem',
              padding: '8px',
              marginBottom: '8px',
              backgroundColor: message.sender === 'User' ? '#e3f2fd' : '#f1f1f1',
              borderRadius: '8px',
              textAlign: 'left', // Keep text left-aligned inside the Paper
              width: 'fit-content', // Allow Paper to only take up space needed
            }}
          >
            {message.sender}: {message.message}
          </Paper>
        </Grid>
      ))}
    </Grid>
  );
}

export default ChatLog;
