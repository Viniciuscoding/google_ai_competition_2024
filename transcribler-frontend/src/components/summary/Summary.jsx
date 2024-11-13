import PropTypes from 'prop-types';
import AgeRating from './AgeRating.jsx';
import Toxicity from './Toxicity.jsx';
import FakeNews from './FakeNews.jsx';
import Summarization from './Summarization.jsx';
import SentimentAnalysis from './SentimentAnalysis.jsx';

import Box from '@mui/material/Box';


import Loading from '../loading/Loading.jsx';

function Summary({ data }) {
  return (
    <>
      {data ? (
        <div>
          <Box mt={2} mb={2}><AgeRating details={data["Age Rating"]}/></Box>
          <Box mb={2}><Toxicity details={data["Toxicity"]}/></Box>
          <Box mb={2}><FakeNews details={data["Fake News"] ? data["Fake News"] : data["Fake news"] }/></Box>
          <Box mb={2}><Summarization details={data["final summary"]}/></Box>
          <Box mb={2}><SentimentAnalysis details={data["Sentiment Analysis"]}/></Box>
        </div>
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
