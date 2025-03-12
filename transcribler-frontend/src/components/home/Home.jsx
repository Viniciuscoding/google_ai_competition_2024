import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useData } from "../../providers/DataContext";

import { getAuth, createUserWithEmailAndPassword } from "firebase/auth";

// api
import { getVideoData } from "../../api";

// mui components
import {
  Box,
  Button,
  CircularProgress,
  Divider,
  Grid2 as Grid,
  IconButton,
  TextField,
  Tooltip,
  Typography,
} from "@mui/material";
import { Send } from "@mui/icons-material";

import { Link, NavLink } from "react-router-dom";

function Home() {
  const [loading, setLoading] = useState(false);
  const [url, setUrl] = useState(null);
  const { setData } = useData();
  const auth = getAuth();
  // console.log(auth.currentUser)
  const navigate = useNavigate();

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const response = await getVideoData(url);
      setData(response);
      navigate("/summary");
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };
  return (
    <>
      <Grid
        container
        direction="column"
        sx={{ width: "100%" }}
        display="flex"
        justifyContent="center"
        alignItems="center"
      >
        <Grid sx={{ padding: "1rem" }}>
          <img src="/imgs/Logo1_35x103.png" alt="logo" />
        </Grid>
        <Divider style={{ width: "100%" }} />
        <Grid
          sx={{
            display: "flex",
            padding: "1rem",
            height: "80vh",
            width: "100vw",
            flexDirection: "row",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <Box
            sx={{
              display: "flex",
              flexDirection: "column",
              gap: 1,
            }}
          >
            <Typography variant="h4" component="h1" sx={{py: 2}}>
              Welcome to Transcribler!
            </Typography>
            {auth.currentUser == null ? (
              <>
                <Button
                  variant="outlined"
                  color="white"
                  component={Link}
                  to="/register"
                >
                  Register
                </Button>
                <Button
                  variant="contained"
                  sx={{ backgroundColor: "black" }}
                  component={Link}
                  to="/login"
                >
                  Login
                </Button>
              </>
            ) : (
              <Box
                sx={{
                  display: "flex",
                  flexDirection: "row",
                  gap: 1,
                  width: "100%",
                }}
              >
                <TextField
                  required
                  label="Video URL"
                  variant="outlined"
                  onChange={(event) => setUrl(event.target.value)}
                  sx={{ flexGrow: 1 }} // This makes the TextField take up available space.
                />
                <Tooltip title="Generate Analysis">
                  <IconButton
                    onClick={handleSubmit}
                    sx={{ width: 56, height: 56, borderRadius: "50%" }}
                  >
                    {loading ? <CircularProgress /> : <Send />}
                  </IconButton>
                </Tooltip>
              </Box>
            )}
          </Box>
        </Grid>
      </Grid>
    </>
  );
}

export default Home;
