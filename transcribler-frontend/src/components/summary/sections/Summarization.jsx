import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';

import "../styles.css";

import { marked } from 'marked';

function Summarization(props) {
  const htmlContent = marked(props.details);

  return (
    <>
      <Typography variant="h6">Summarization</Typography>
      <Paper
        elevation={0}
        sx={{
          backgroundColor: "#F1F1F1",
          padding: "1rem"
        }}
      >
        <div dangerouslySetInnerHTML={{ __html: htmlContent }} />
      </Paper>
    </>
  );
}

export default Summarization;
