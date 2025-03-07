import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useData } from "../../providers/DataContext";

// api
import { getVideoData } from "../../api";

// mui components
import {
  Box,
  CircularProgress,
  Divider,
  Grid2 as Grid,
  IconButton,
  TextField,
  Tooltip,
} from "@mui/material";
import { Send } from "@mui/icons-material";

import { Link, NavLink } from "react-router-dom";

function Home() {
  const [loading, setLoading] = useState(false);
  const [url, setUrl] = useState(null);
  const { setData } = useData();

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
        <Grid item sx={{ padding: "1rem" }}>
          <img src="/imgs/Logo1_35x103.png" alt="logo" />
        </Grid>
        <Divider style={{ width: "100%" }} />
        <Grid
          item
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
              gap: 1,
            }}
          >
            <TextField
              required
              label="Video URL"
              variant="outlined"
              sx={{ width: "25vw" }}
              onChange={(event) => setUrl(event.target.value)}
            />
            <Tooltip title="Generate Analysis">
              <IconButton onClick={handleSubmit} sx={{ width: 56, height: 56, borderRadius: "50%" }}>
                {loading ? <CircularProgress /> : <Send />}
              </IconButton>
            </Tooltip>
          </Box>
        </Grid>
      </Grid>
    </>
  );
}

export default Home;
