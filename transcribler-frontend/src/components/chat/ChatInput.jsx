import { useState } from "react";
import { GoogleGenerativeAI } from "@google/generative-ai";

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

  const videoUrl = data.url;

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
          parts: [{ text: "You are a chat bot named Transcribler. Introduce yourself as such whenever you are greeted. You specialize in transcribing, summarizing, providing age and toxicity ratings, and providing sentiment analysis on YouTube videos. This is your sole function. Keep your responses brief and concise, don't just restate data provided to you. The following is data on the video you were given to analyze:" + JSON.stringify(data) }], 
        },
        {
          role: "model",
          parts: [{ text: "Great to meet you. What would you like to know?" }], 
        },
      ],
      generationConfig: {
        maxOutputTokens: 100,
      },
    });

    const result = await chat.sendMessage(msg);
    const response = await result.response;
    let text = response.text();
    text = `
      ${text}
    `
    return text
  }

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
        zIndex: 10
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
