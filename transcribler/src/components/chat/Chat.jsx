import {useState} from 'react';

import './styles.css'
import ChatInput from './ChatInput'
import ChatLog from './ChatLog'

function Chat() {
  const [message, setMessage] = useState("");
  return (
    <>
      <ChatLog sendMessage={message}/>
      <ChatInput retrieveMessage={(e) => setMessage(e)}/>
    </>
  );
}

export default Chat;
