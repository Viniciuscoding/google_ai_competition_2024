import {useState} from 'react';
import { useLocation } from 'react-router-dom';

import './styles.css'
import Header from '../../components/header/Header';
import ChatInput from './ChatInput'
import ChatLog from './ChatLog'

function Chat() {
  const [message, setMessage] = useState("");
  const location = useLocation();
  const data = location.state?.data;
  return (
    <>
      <Header title={data.title} data={data}/>
      <ChatLog sendMessage={message}/>
      <ChatInput data={data} retrieveMessage={(e) => setMessage(e)}/>
    </>
  );
}

export default Chat;
