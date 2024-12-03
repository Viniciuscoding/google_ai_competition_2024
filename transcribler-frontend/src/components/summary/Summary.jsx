import { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';

import PropTypes from 'prop-types';
import Header from '../../components/header/Header';
import AgeRating from './sections/AgeRating.jsx';
import Toxicity from './sections/Toxicity.jsx';
import FakeNews from './sections/FakeNews.jsx';
import Summarization from './sections/Summarization.jsx';
import SentimentAnalysis from './sections/SentimentAnalysis.jsx';

import Box from '@mui/material/Box';


import Loading from '../loading/Loading.jsx';
import axios from 'axios';

function Summary() {
  const location = useLocation();
  const url = location.state?.url;
  const [data, setData] = useState(location.state?.data ?? null);

  useEffect(() => {
    const abortController = new AbortController();

    const fetchData = async () => {
      try {
        console.log("getting video data for ", url);
        const response = await axios.post(`http://127.0.0.1:5000/`, 
          { url: url },
          { signal: abortController.signal }
        );
        setData(response.data);
      } catch (e) {
        if (e.name !== 'AbortError') {
          console.error("response failed", e);
        }
      }
    };

    if (!data) fetchData();

    return () => {
      abortController.abort(); 
    };
  }, []);

  return (
    <>
      {data ? (
        <>
          <Header title={data.title} data={data}/>
          <Box m={1}>
            <Box mt={2} mb={2}><AgeRating details={data["Age Rating"]}/></Box>
            <Box mb={2}><Toxicity details={data["Toxicity"]}/></Box>
            <Box mb={2}><FakeNews details={data["Fake News"] ? data["Fake News"] : data["Fake news"] }/></Box>
            <Box mb={2}><Summarization details={data["final summary"]}/></Box>
            <Box mb={2}><SentimentAnalysis details={data["Sentiment Analysis"]}/></Box>
          </Box>
        </>
      ) : (
        <Loading />
      )}
    </>
  );
}

Summary.propTypes = {
  data: PropTypes.object, // Add more specific validation based on the data structure
};

export default Summary;
