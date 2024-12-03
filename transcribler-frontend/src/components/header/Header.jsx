// import { useState } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import './styles.css';

import Divider from '@mui/material/Divider';
import Grid from '@mui/material/Grid2';
import Link from '@mui/material/Link';

function Header({title, data}) {
  const location = useLocation();

  return (
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
      <Grid
        container
        justifyContent="center"
        alignItems="center"
        sx={{ padding: '0 20px', fontWeight: 'bold'}}
        mb={2}
      >
        <Grid item>
          {title}
        </Grid>
      </Grid>
      <Divider/>
      <Grid
        container
        justifyContent="space-between"
        alignItems="center"
        sx={{ padding: '0 20px', width: '100%' }}
        mt={2}
      >
        <Grid item>
          <Link 
            component={NavLink} 
            to='/summary' 
            state= {{data}}
            className="navlink"
            sx={{ display: 'flex', alignItems: 'center', backgroundColor: location.pathname == '/summary' ? '#FFE1E1' : null, padding: '0.5rem', borderRadius: '10%'}}
          >
            <img src="/imgs/Checklist.svg" alt="summary icon" style={{ marginRight: '8px' }} />
            Summary
          </Link>
        </Grid>
        
        <Grid item>
          <Link 
            component={NavLink} 
            to='/chat' 
            state= {{data}}
            className="navlink" 
            sx={{ display: 'flex', alignItems: 'center', backgroundColor: location.pathname == '/chat' ? '#FFE1E1' : null, padding: '0.5rem', borderRadius: '10%' }}
          >
            <img src="/imgs/Group 6770.svg" alt="chat icon" style={{ marginRight: '8px' }} />
            Chat
          </Link>
        </Grid>
      </Grid>
      
    </Grid>
  );
}

export default Header;
