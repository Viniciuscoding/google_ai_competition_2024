import { useState, useContext, useEffect } from "react";
import { useNavigate, Link, NavLink } from "react-router-dom";
import { useData } from "../../providers/DataContext";

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
import { Logout, Send } from "@mui/icons-material";

import { AuthContext } from "../../providers/AuthContext";

function Home({ url }) {
  const [loadingAnalysis, setLoadingAnalysis] = useState(false);
  // const [url, setUrl] = useState(null);
  const { setData } = useData();
  const { user, loading, signOut } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async () => {
    setLoadingAnalysis(true);
    try {
      const response = await getVideoData(url);
      setData(response);
      navigate("/summary");
    } catch (e) {
      console.error(e);
    }
    setLoadingAnalysis(false);
  };

  useEffect(() => {
    if (url && !loadingAnalysis) {
      handleSubmit();
    }
  }, [url]);

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
        <Grid
          container
          sx={{ padding: "1rem", display: "flex", alignItems: "center" }}
        >
          <Grid xs={12} sx={{ display: "flex", justifyContent: "center" }}>
            <img src="/imgs/Logo1_35x103.png" alt="logo" />
          </Grid>
          {user && (
            <Grid sx={{ position: "absolute", right: "1rem" }}>
              <IconButton onClick={() => signOut()}>
                <Logout />
              </IconButton>
            </Grid>
          )}
        </Grid>
        {/* URL: {url} */}
        <Divider style={{ width: "100%" }} />
        {loading ? (
          <CircularProgress />
        ) : (
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
              <Typography variant="h4" component="h1" sx={{ py: 2 }}>
                Welcome to Transcribler!
              </Typography>
              {user == null ? (
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
                    value={url}
                    disabled
                  />
                  <Tooltip title="Generate Analysis">
                    <IconButton
                      onClick={handleSubmit}
                      sx={{ width: 56, height: 56, borderRadius: "50%" }}
                    >
                      {loadingAnalysis ? <CircularProgress /> : <Send />}
                    </IconButton>
                  </Tooltip>
                </Box>
              )}
            </Box>
          </Grid>
        )}
      </Grid>
    </>
  );
}

export default Home;
