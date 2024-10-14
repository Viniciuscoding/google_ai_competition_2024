import Box from '@mui/material/Box';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputAdornment from '@mui/material/InputAdornment';
import IconButton from '@mui/material/IconButton';
import InputLabel from '@mui/material/InputLabel';
import FormControl from '@mui/material/FormControl';

import './styles.css'

function ChatInput() {
  return (
    <>
      <Box
        sx={{
          position: "fixed",
          bottom: 0,
          left: "50%",
          transform: "translateX(-50%)", 
          maxWidth: "600px",
          width: "100%",
          display: "flex",
          alignItems: "center",
          padding: "8px",
          backgroundColor: "#fff"
        }}
        component="footer"
      >
        <FormControl fullWidth variant="outlined">
          <InputLabel htmlFor="outlined-multiline-flexible">Ask me anything!</InputLabel>
          <OutlinedInput
            id="outlined-multiline-flexible"
            multiline
            maxRows={4}
            label="Ask me anything!"
            endAdornment={
              <InputAdornment position="end">
                <IconButton aria-label="send message" edge="end">
                  <img src="/imgs/Microphone_icon_20x20.svg" alt="send" />
                </IconButton>
                <IconButton aria-label="attach file" edge="end">
                  <img src="/imgs/send_icon_20x20.svg" alt="attach" />
                </IconButton>
              </InputAdornment>
            }
          />
        </FormControl>
        <img src="/imgs/Human02_icon_25x25.svg" style={{ marginLeft: "10px", width: "25px", height: "25px" }} alt="user icon" />
      </Box>
    </>
  );
}

export default ChatInput;
