import { useState, useEffect } from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';

/* component routes */
import Header from './components/header/Header';
import History from './components/history/History';
import Summary from './components/summary/Summary';
import Chat from './components/chat/Chat';

/* mui */
import Grid from '@mui/material/Grid2';
import axios from 'axios';

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    const abortController = new AbortController();

    const fetchData = async () => {
      try {
        console.log("getting prof data");
        const response = await axios.get(`http://127.0.0.1:5000`, {
          signal: abortController.signal,
        });
        setData(response.data);
      } catch (e) {
        if (e.name !== 'AbortError') {
          console.error("response failed", e);
        }
      }
    };

    fetchData();

    return () => {
      abortController.abort(); 
    };
  }, []); 

  console.log(data)

  return (
    <BrowserRouter>
      <Grid container direction="column">
        {data ? <Header title={data.title}/> : <></>}
        <Routes>
          <Route path="/" element={<Summary data={data} />} />
          <Route path="/history" element={<History />} />
          <Route path="/chat" element={<Chat />} />
        </Routes>
      </Grid>
    </BrowserRouter>
  );
}

export default App;

