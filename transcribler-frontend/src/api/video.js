import axios from "axios";

const backendURL = import.meta.env.VITE_BACKEND_URL;

export const getVideoData = async (url) => {
  try {
    const response = await axios.post(
      `${backendURL}/`,
      { url: url },
      {
        responseType: "blob", // Set the response type to 'blob'
      }
    );
    return response.data;
  } catch (e) {
    console.error(e);
  }
};

export const getTest = async (url) => {
  try {
    const response = await fetch(`${backendURL}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ url: url })
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response;
  } catch (e) {
    console.error(e);
  }
  try {
    const response = await axios.post(
      `${backendURL}/`,
      { url: url },
      {
        responseType: "blob", // Set the response type to 'blob'
      }
    );
    return response.data;
  } catch (e) {
    console.error(e);
  }
};
