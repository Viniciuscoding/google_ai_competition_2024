import { useState } from "react";

// mui components
import { 
  Box,
  Button,
  Divider, 
  Grid2 as Grid, 
  TextField,
  Typography,
} from "@mui/material";

import { NavLink } from "react-router-dom";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [emailError, setEmailError] = useState(false);
  const [passwordError, setPasswordError] = useState(false);

  const handleSubmit = () => {
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
          <NavLink to="/">
            <img src="/imgs/Logo1_35x103.png" alt="logo" />
          </NavLink>
        </Grid>
        <Divider style={{ width: "100%" }} />
        <Grid>
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
              required
              error={emailError}
              helperText={emailError && "Invalid email."}
              label="Email"
              onChange={(e) => setEmail(e.target.value)}
            />
            <TextField
              required
              error={passwordError}
              helperText={passwordError && "Invalid password."}
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
          </Box>
        </Grid>
      </Grid>
    </>
  );
}

export default Login;
