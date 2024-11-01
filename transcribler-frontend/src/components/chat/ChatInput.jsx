/* eslint-disable react/prop-types */
import { useState } from "react";
import { GoogleGenerativeAI } from "@google/generative-ai";

import Box from '@mui/material/Box';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputAdornment from '@mui/material/InputAdornment';
import IconButton from '@mui/material/IconButton';
import InputLabel from '@mui/material/InputLabel';
import FormControl from '@mui/material/FormControl';

import './styles.css'

function ChatInput({retrieveMessage}) {
  const [inputValue, setInputValue] = useState('');

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const [geminiKey] = useState(import.meta.env.VITE_GEMINI_API_KEY);
  const [genAI] = useState(new GoogleGenerativeAI(geminiKey));
  const [model] = useState(genAI.getGenerativeModel({ model: "gemini-pro"}));

  const testBot = async () => {
    if (inputValue.trim()) {
      retrieveMessage({sender: "User", message: inputValue}); 
      setInputValue(''); 
      const response = await sendMessage(inputValue);
      retrieveMessage({sender: "Gemini", message: response});
    } else {
      console.log("No message to send");
    }
  };
  

  const sendMessage = async (msg) => {
    const chat = model.startChat({
      history: [
        {
          role: "user",
          parts: [{ text: "Hello" }],
        },
        {
          role: "model",
          parts: [{ text: "Great to meet you. What would you like to know?" }],
        },
      ],
      generationConfig: {
        maxOutputTokens: 250,
      },
    });
  
    const result = await chat.sendMessage(msg);
    const response = await result.response;
    let text = response.text();
    text = `
      ${text}
    `
    // console.log(text)
    return text
  }
  
  return (
    <>
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
                <div>
                  <IconButton
                    aria-label="microphone"
                    edge="end"
                  >
                    <img
                      src="/imgs/Microphone_icon_20x20.svg"
                      alt="send"
                    />
                  </IconButton>
                </div>
                <IconButton 
                  aria-label="send message" 
                  edge="end"
                  onClick={testBot}
                >
                  <img src="/imgs/send_icon_20x20.svg" alt="attach" />
                </IconButton>
              </InputAdornment>
            }
          />
        </FormControl>
        <img
          src="/imgs/Human02_icon_25x25.svg"
          style={{ marginLeft: '10px', width: '25px', height: '25px' }}
          alt="user icon"
        />
      </Box>
    </>
  );
}

export default ChatInput;
