import { BrowserRouter, Route, Routes } from 'react-router-dom';

/* component routes */ 
import Header from './components/header/Header';
import History from './components/history/History';
import Summary from './components/summary/Summary';
import Chat from './components/chat/Chat';

/* mui */
import Grid from '@mui/material/Grid2';

function App() {
  return (
    <BrowserRouter>
      <Grid
        container
        direction="column"
        // alignItems="center"
      >
        <Header />
        <Routes>
          <Route path="/" element={<Summary />} />
          <Route path="/history" element={<History />} />
          <Route path="/chat" element={<Chat />} />
        </Routes>
      </Grid>
    </BrowserRouter>
  );
}

export default App
