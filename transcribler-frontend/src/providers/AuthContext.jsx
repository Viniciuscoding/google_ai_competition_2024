import React, { useState, useEffect, createContext } from "react";
import { useNavigate } from "react-router-dom";
import { onAuthStateChanged } from "firebase/auth";
import { auth } from "../firebase/BaseConfig";
import { firebaseSignUp, firebaseSignIn, firebaseSignOut } from "../firebase/AuthService";

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
  const navigate = useNavigate();

  // **Sign Up**
  const signUp = async (creds) => {
    setIsLoading(true);
    return firebaseSignUp(creds) // ✅ Ensures a Promise is returned
      .then((signUpResult) => {
        const { user } = signUpResult;
        if (user) {
          console.log(1);
          setCurrentUser(user);
        } else {
          console.log(2);
        }
      })
      .catch((error) => {
        console.error(error);
        throw error; // ✅ Error propagates correctly
      })
      .finally(() => {
        setIsLoading(false);
      });
  };

  // **Sign In**
  const signIn = async (creds) => {
    setIsLoading(true);
    return firebaseSignIn(creds) // ✅ Ensures a Promise is returned
      .then((signInResult) => {
        const { user } = signInResult;
        if (user) {
          setCurrentUser(user);
          console.log(1);
        } else {
          console.log(2);
        }
      })
      .catch((error) => {
        console.error(error);
        throw error; // ✅ Error propagates correctly
      })
      .finally(() => {
        setIsLoading(false);
      });
  };

  // **Sign Out**
  const signOut = async () => {
    setIsLoading(true);
    return firebaseSignOut() // ✅ Ensures a Promise is returned
      .then(() => {
        setCurrentUser(null);
        navigate("/signin", { replace: true });
      })
      .catch((error) => {
        console.error(error);
        throw error; // ✅ Error propagates correctly
      })
      .finally(() => {
        setIsLoading(false);
      });
  };

  // **Auth Values**
  const authValues = {
    user: currentUser,
    loading: isLoading,
    signIn,
    signUp,
    signOut,
  };

  // **Auth State Listener**
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setCurrentUser(user);
      setIsAuthLoading(false);
    });
    return unsubscribe;
  }, []);

  return <AuthContext.Provider value={authValues}>{children}</AuthContext.Provider>;
};
