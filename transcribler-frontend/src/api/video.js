import axios from 'axios';

const backendURL = import.meta.env.VITE_BACKEND_URL;

export const getVideoData = async (url) => {
  try{
    const response = await axios.post(`${backendURL}/`, { url: url });
    return response.data;
  } catch (e){
    console.error(e);
  }
};