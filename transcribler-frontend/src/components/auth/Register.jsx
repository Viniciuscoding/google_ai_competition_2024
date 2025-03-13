import { useState, useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../../providers/AuthContext";

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

import { NavLink } from "react-router-dom";

const emailRegex =
  /(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])/;

const passwordRegex =
  /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/;

function Register() {
  const { signUp } = useContext(AuthContext);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [emailError, setEmailError] = useState(false);
  const [passwordError, setPasswordError] = useState(false);
  const [confirmPasswordError, setConfirmPasswordError] = useState(false);

  const [registerFailed, setRegisterFailed] = useState(false);

  const navigate = useNavigate();

  const handleSubmit = () => {
    // form validation
    setEmailError(!email.match(emailRegex));
    setPasswordError(!password.match(passwordRegex));
    setConfirmPasswordError(password !== confirmPassword);
  };

  useEffect(() => {
    if (!emailError && !passwordError && !confirmPasswordError) {
      async () => {
        if (email && password && confirmPassword) {
          try {
            signUp({ email, password });
            navigate("/");
          } catch (e) {
            console.error(e);
            setRegisterFailed(true);
          }
        }
      };
    }
  }, [emailError, passwordError, confirmPasswordError]);

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
              // py: 5,
              gap: 2,
              "& .MuiTextField-root": { m: 1, width: "25ch" },
            }}
            noValidate
            autoComplete="off"
          >
            <Typography variant="h4" component="h1">
              Register
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
              helperText={
                passwordError &&
                "Password must have minimum 8 characters, at least one letter, 1 number and 1 special character."
              }
              label="Password"
              type="password"
              onChange={(e) => setPassword(e.target.value)}
            />
            <TextField
              required
              error={confirmPasswordError}
              helperText={
                confirmPasswordError && "Password confirmation does not match."
              }
              label="Confirm password"
              type="password"
              onChange={(e) => setConfirmPassword(e.target.value)}
            />
            <Button
              variant="contained"
              sx={{ backgroundColor: "black" }}
              onClick={handleSubmit}
            >
              Register
            </Button>
            {registerFailed && (
              <Alert severity="error">
                Registration failed. Please try again.
              </Alert>
            )}
          </Box>
        </Grid>
      </Grid>
    </>
  );
}

export default Register;
