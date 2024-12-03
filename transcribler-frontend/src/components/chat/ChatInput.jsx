/* eslint-disable react/prop-types */
import { useState } from "react";
import Box from '@mui/material/Box';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputAdornment from '@mui/material/InputAdornment';
import IconButton from '@mui/material/IconButton';
import InputLabel from '@mui/material/InputLabel';
import FormControl from '@mui/material/FormControl';

import './styles.css';

function ChatInput({ retrieveMessage, data }) {
  const [inputValue, setInputValue] = useState('');

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  // Hardcoded YouTube URL for testing
  const videoUrl = data.url;

  const testBot = async () => {
    if (inputValue.trim()) {
      retrieveMessage({ sender: "User", message: inputValue });
      setInputValue('');

      try {
        const response = await fetch('http://localhost:5000/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: inputValue,
            video_url: videoUrl,
          }),
        });

        if (response.ok) {
          const responseData = await response.json();
          retrieveMessage({ sender: "Gemini", message: responseData.response });
        } else {
          retrieveMessage({ sender: "Gemini", message: "Error: Unable to get a response." });
        }
      } catch (error) {
        console.error("Error communicating with the backend:", error);
        retrieveMessage({ sender: "Gemini", message: "Sorry, something went wrong." });
      }
    } else {
      console.log("No message to send");
    }
  };

  return (
    <Box
      sx={{
        position: 'fixed',
        bottom: 0,
        left: '50%',
        transform: 'translateX(-50%)',
        maxWidth: '600px',
        width: '100%',
        display: 'flex',
        alignItems: 'center',
        padding: '8px',
        backgroundColor: '#fff',
      }}
      component="footer"
    >
      <FormControl fullWidth variant="outlined">
        <InputLabel htmlFor="outlined-multiline-flexible">
          Ask me anything!
        </InputLabel>
        <OutlinedInput
          id="outlined-multiline-flexible"
          multiline
          maxRows={4}
          label="Ask me anything!"
          value={inputValue}
          onChange={handleInputChange}
          endAdornment={
            <InputAdornment position="end">
              <IconButton aria-label="send message" edge="end" onClick={testBot}>
                <img src="/imgs/send_icon_20x20.svg" alt="send" />
              </IconButton>
            </InputAdornment>
          }
        />
      </FormControl>
    </Box>
  );
}

export default ChatInput;
