
// import React, {useState, useEffect} from 'react';

import AgeRating from './AgeRating.jsx'
import Toxicity from './Toxicity.jsx'
import FakeNews from './FakeNews.jsx'
import Summarization from './Summarization.jsx'
import SentimentAnalysis from './SentimentAnalysis.jsx'

import Box from '@mui/material/Box';

function Summary() {
  return (
    <div>
      <Box mt={2} mb={2}><AgeRating /></Box>
      <Box mb={2}><Toxicity /></Box>
      <Box mb={2}><FakeNews /></Box>
      <Box mb={2}><Summarization /></Box>
      <Box mb={2}><SentimentAnalysis /></Box>
    </div>
  );
}

export default Summary;
