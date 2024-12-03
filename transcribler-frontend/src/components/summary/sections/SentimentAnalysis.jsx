
// import React from 'react';

import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';

import "../styles.css"


function SentimentAnalysis(props) {
  return (
    <>
      <Typography variant="h6">Sentiment Analysis</Typography>
      <Paper
        elevation={0}
        sx={{
          backgroundColor: "#F1F1F1",
          padding: "1rem"
        }}
      >
        {props.details}
      </Paper>
    </>
  );
}

export default SentimentAnalysis;
