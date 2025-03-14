import { useState, useEffect } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";

import { AuthProvider } from "./providers/AuthContext";
import { DataProvider } from "./providers/DataContext";

/* component routes */
import Home from "./components/home/Home";
import History from "./components/history/History";
import Summary from "./components/summary/Summary";
import Chat from "./components/chat/Chat";
import Login from "./components/auth/Login";
import Register from "./components/auth/Register";

// theme
import theme from "./theme";

/* mui */
import { Grid2 as Grid, ThemeProvider } from "@mui/material";

function App() {
  const [url, setUrl] = useState("");
  useEffect(() => {
    // Send a message to the background script
    chrome.runtime.sendMessage({ type: "GET_ACTIVE_TAB_URL" }, (response) => {
      if (response && response.url) {
        console.log("URL received:", response.url);
        setUrl(response.url);
      } else {
        console.log("No URL received");
        setUrl(null);
      }
    });
  }, []);

  return (
    <BrowserRouter>
      <ThemeProvider theme={theme}>
        <AuthProvider>
          <DataProvider>
            <Grid container direction="column">
              <Routes>
                <Route path="/" element={<Home url={url}/>} />
                <Route path="/summary" element={<Summary />} />
                <Route path="/history" element={<History />} />
                <Route path="/chat" element={<Chat />} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="*" element={<Home />} />{" "}
                {/* TODO: Create an actual 404 Not Found page */}
              </Routes>
            </Grid>
          </DataProvider>
        </AuthProvider>
      </ThemeProvider>
    </BrowserRouter>
  );
}

export default App;
