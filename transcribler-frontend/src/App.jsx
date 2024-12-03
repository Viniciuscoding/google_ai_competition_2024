import { useState, useEffect } from 'react';
import { HashRouter, Route, Routes } from 'react-router-dom';

/* component routes */
import Home from './components/home/Home';
// import Header from './components/header/Header';
import History from './components/history/History';
import Summary from './components/summary/Summary';
import Chat from './components/chat/Chat';

/* mui */
import Grid from '@mui/material/Grid2';

function App() {
  const [url, setUrl] = useState("");

  useEffect(() => {
    // Send a message to the background script
    chrome.runtime.sendMessage(
      { type: "GET_ACTIVE_TAB_URL" },
      (response) => {
        if (response?.url) {
          setUrl(response.url);
        } else {
          setUrl("");
        }
      }
    );
  }, []);

  return (
    <HashRouter>
      <Grid container direction="column">
        {/* {data ? <Header title={data.title}/> : <></>} */}
        <Routes>
          <Route path="/" element={<Home url={url}/>} />
          <Route path="/summary" element={<Summary />} />
          <Route path="/history" element={<History />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="*" element={<Home url={url}/>} /> 
        </Routes>
      </Grid>
    </HashRouter>
  );
}

export default App;

