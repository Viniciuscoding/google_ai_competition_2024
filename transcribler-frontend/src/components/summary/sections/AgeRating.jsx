
// import React from 'react';

import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';

import Markdown from 'react-markdown'

import "../styles.css"


function AgeRating(props) {
  return (
    <>
      <Typography variant="h6">Age Rating</Typography>
      <Paper
        elevation={0}
        sx={{
          backgroundColor: "#F1F1F1",
          padding: "1rem",
          width: "300px"
        }}
      >
        <Markdown>{props.details}</Markdown>
      </Paper>
    </>
  );
}

export default AgeRating;
