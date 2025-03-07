import { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { useData } from "../../providers/DataContext.jsx";

import PropTypes from 'prop-types';

// mui components
import Box from '@mui/material/Box';

// custom components
import Loading from '../loading/Loading.jsx';
import Header from '../header/Header.jsx';
import AgeRating from './sections/AgeRating.jsx';
import Toxicity from './sections/Toxicity.jsx';
import FakeNews from './sections/FakeNews.jsx';
import Summarization from './sections/Summarization.jsx';
import SentimentAnalysis from './sections/SentimentAnalysis.jsx';

function Summary() {
  const location = useLocation();
  const url = location.state?.url;
  const { data } = useData();

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
