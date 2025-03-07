import { useState, useEffect } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";

import { DataProvider } from "./providers/DataContext";

/* component routes */
import Home from "./components/home/Home";
import History from "./components/history/History";
import Summary from "./components/summary/Summary";
import Chat from "./components/chat/Chat";

/* mui */
import { Grid2 as Grid } from "@mui/material";

function App() {
  return (
    <DataProvider>
      <BrowserRouter>
        <Grid container direction="column">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/summary" element={<Summary />} />
            <Route path="/history" element={<History />} />
            <Route path="/chat" element={<Chat />} />
            <Route path="*" element={<Home />} />{" "} {/* TODO: Create an actual 404 Not Found page */}
          </Routes>
        </Grid>
      </BrowserRouter>
    </DataProvider>
  );
}

export default App;
