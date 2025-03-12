import React, { useState, useEffect, createContext } from "react";
import { useNavigate } from "react-router-dom";

import { onAuthStateChanged } from "firebase/auth";

import { auth } from "../firebase/BaseConfig";

import {
  firebaseSignUp,
  firebaseSignIn,
  firebaseSignOut,
} from "../firebase/AuthService";

export const AuthContext = createContext({
  user: auth.currentUser,
  loading: false,
  signIn: () => {},
  signUp: () => {},
  signOut: () => {},
});

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isAuthLoading, setIsAuthLoading] = useState(true);
  // const navigate = useNavigate();

  //Sign up
  const signUp = (creds) => {
    setIsLoading(true);
    firebaseSignUp(creds)
      .then(async (signUpResult) => {
        const { user } = signUpResult; //object destructuring
        if (user) {
          setCurrentUser(user);
          //redirect the user on the targeted route
          // navigate("/dashboard", { replace: true });
        } else {
          //do something if user is empty like an alert
        }
        setIsLoading(false);
      })
      .catch((error) => {
        //check for error
        if (error.code === "auth/email-already-in-use") {
          //show an alert or console
        } else if (error.code === "auth/too-many-requests") {
          //do something like an alert
        }
        // you can check for more error like email not valid or something
        setIsLoading(false);
      });
  };

  //Sign in
  const signIn = async (creds, onSuccess) => {
    setIsLoading(true);
    firebaseSignIn(creds)
      .then((signInResult) => {
        const { user } = signInResult;
        if (user) {
          setCurrentUser(user);
          //redirect user to targeted route
          navigate("/dashboard", { replace: true });
        } else {
          //do something
        }
        setIsLoading(false);
      })
      .catch((error) => {
        if (error.code === "auth/wrong-password") {
          //show error
        } else if (error.code === "auth/too-many-requests") {
          //show error
        }
        setIsLoading(false);
      });
  };

  //Sign out
  const signOut = async () => {
    setIsLoading(true);
    try {
      await firebaseSignOut();
      setCurrentUser(null);
      navigate("/signin", { replace: true });
    } catch (error) {
      setIsLoading(false);
      //show error alert
    }
  };

  //create Auth Values
  const authValues = {
    user: currentUser,
    loading: isLoading,
    signIn,
    signUp,
    signOut,
  };

  useEffect(() => {
    //onAuthStateChanged check if the user is still logged in or not
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setCurrentUser(user);
      setIsAuthLoading(false);
    });
    return unsubscribe;
  }, []);

  // //If loading for the first time when visiting the page
  // if (isAuthLoading) return <PageLoading />;

  return (
    <AuthContext.Provider value={authValues}>{children}</AuthContext.Provider>
  );
};
