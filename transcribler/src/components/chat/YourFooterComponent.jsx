
// import React, {useState, useEffect} from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';

// import './styles.css'

function Chat() {
  return (
    <>
      <Box
        sx={{
          position: "fixed", bottom: 0
        }}
        component="footer"
      >
        <TextField
          id="outlined-multiline-flexible"
          label="Multiline"
          multiline
          maxRows={4}
        />
      </Box>
    </>
  );
}

export default Chat;
