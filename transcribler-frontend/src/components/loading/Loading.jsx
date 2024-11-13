import CircularProgress from '@mui/material/CircularProgress'; // Optional, using MUI CircularProgress as loader

const Loading = () => {
  return (
    <div style={styles.loaderContainer}>
      <CircularProgress sx={{color:"red"}}/> {/* MUI Circular Progress Spinner */}
    </div>
  );
};

const styles = {
  loaderContainer: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100vh', // Full viewport height
  },
};

export default Loading;
