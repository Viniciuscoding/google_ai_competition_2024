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
    <Grid container direction="column" spacing={2} mt={4} sx={{ textAlign: 'left', padding: '0 20px' }}>
      {log.map((message, index) => (
        <Grid
          key={index}
          item
          display="flex"
          justifyContent={message.sender === 'User' ? 'flex-end' : 'flex-start'}
        >
          <div>test</div>
          <Paper
            elevation={0}
            sx={{
              maxWidth: '25rem',
              padding: '8px',
              marginBottom: '8px',
              backgroundColor: message.sender === 'User' ? '#e3f2fd' : '#f1f1f1',
              borderRadius: '8px',
              textAlign: 'left',
              width: 'fit-content', 
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
