import { useState, useEffect } from 'react';
import Grid from '@mui/material/Grid2';
import Paper from '@mui/material/Paper';

import './styles.css';

function ChatLog(props) {
  const [log, setLog] = useState([]);

  useEffect(() => {
    if (props.sendMessage) {
      console.log(props.sendMessage);
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
          alignItems="center" // Centering content vertically
        >
          {message.sender === 'User' ? <></> : 
            <img
              src="/imgs/Human01_icon_25x25.svg"
              style={{ marginRight: '10px', width: '25px', height: '25px', alignSelf: 'center' }}
              alt="user icon"
            />
          }
          <Paper
            elevation={0}
            sx={{
              maxWidth: '25rem',
              padding: '8px',
              backgroundColor: message.sender === 'User' ? '#e3f2fd' : '#f1f1f1',
              borderRadius: '8px',
              textAlign: 'left',
              width: 'fit-content',
            }}
          >
            {message.message}
          </Paper>
          {message.sender === 'User' ? (
            <img
              src="/imgs/Human02_icon_25x25.svg"
              style={{ marginLeft: '10px', width: '25px', height: '25px', alignSelf: 'center' }}
              alt="user icon"
            />
          ) : (
            <></>
          )}
        </Grid>
      ))}
    </Grid>
  );
}

export default ChatLog;
