import Divider from '@mui/material/Divider';
import Grid from '@mui/material/Grid2';
import Link from '@mui/material/Link';

import { NavLink } from 'react-router-dom';


function Home({ url }) {
  return (
    <>
      <Grid container direction="column" sx={{ width: '100%' }}>
        <Grid
          container
          justifyContent="center"
          alignItems="center"
          sx={{ padding: '1rem' }}
        >
          <Grid item>
            <img src="/imgs/Logo1_35x103.png" alt="logo" />
          </Grid>
        </Grid>
        <Divider/>    
        <Grid
          container
          justifyContent="center"
          alignItems="center"
          sx={{ padding: '2rem', fontWeight: 'bold', display:"flex", height:"75vh"}}
          mb={2}
        >
          <Link 
            component={NavLink} 
            to='/summary'
            state= {{url}}
            className="navlink"
            sx={{ display: 'flex', alignItems: 'center', backgroundColor: '#FFE1E1', padding: '0.5rem', marginY:"auto", borderRadius: '10%', fontSize:"1.5rem"}}
          >
            Generate Analysis
          </Link>
        </Grid>   
      </Grid>
    </>
  );
}


export default Home;
