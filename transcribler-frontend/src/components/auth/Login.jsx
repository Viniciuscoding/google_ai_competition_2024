import { useState, useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { NavLink } from "react-router-dom";

// mui components
import {
  Alert,
  Box,
  Button,
  Divider,
  Grid2 as Grid,
  TextField,
  Typography,
} from "@mui/material";

import { AuthContext } from "../../providers/AuthContext";

function Login() {
  const { user, loading, signIn } = useContext(AuthContext);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loginFailed, setLoginFailed] = useState(false);

  const navigate = useNavigate();

  const handleSubmit = async () => {
    try {
      await signIn({ email, password });
    } catch (e) {
      console.error(e);
      setLoginFailed(true);
    }
  };

  useEffect(() => {
    if (user) {
      navigate("/home");
    }
  }, [user]);

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
          <NavLink to="/">
            <img src="/imgs/Logo1_35x103.png" alt="logo" />
          </NavLink>
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
            component="form"
            sx={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              py: 5,
              gap: 2,
              "& .MuiTextField-root": { m: 1, width: "25ch" },
            }}
            noValidate
            autoComplete="off"
          >
            <Typography variant="h4" component="h1">
              Login
            </Typography>
            <TextField
              label="Email"
              onChange={(e) => setEmail(e.target.value)}
            />
            <TextField
              required
              label="Password"
              type="password"
              onChange={(e) => setPassword(e.target.value)}
            />
            <Button
              variant="contained"
              sx={{ backgroundColor: "black" }}
              onClick={handleSubmit}
            >
              Login
            </Button>
            {loginFailed && (
              <Alert severity="error">Incorrect email or password.</Alert>
            )}
          </Box>
        </Grid>
      </Grid>
    </>
  );
}

export default Login;
