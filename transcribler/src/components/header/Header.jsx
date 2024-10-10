
import {useState} from 'react';
import { NavLink } from 'react-router-dom';

// import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid2';
import Link from '@mui/material/Link';

// import SummarizeIcon from '@mui/icons-material/Summarize';

function Header() {
  const [isSummary, setIsSummary] = useState(true);
  return (
    <Grid
      container
      alignItems="center"
      direction="row"
      spacing={4}
    > 
      <Grid display="flex" justifyContent="center"  size={2}>
        <Link component={NavLink} to='/history' className="navlink">
          History
        </Link>
      </Grid>
      <Grid display="flex" justifyContent="center"  size={8}>
        <Link component={NavLink} to='/'>
          <img src="/imgs/Logo1_35x103.png" alt="img"/>
        </Link>
      </Grid>
      <Grid display="flex" justifyContent="center"  size={2}>
        {isSummary ? 
          <Link component={NavLink} to='/summary' className="navlink" onClick={()=>setIsSummary(false)}>
            Summary
          </Link>
          :
          <Link component={NavLink} to='/chat' className="navlink" onClick={()=>setIsSummary(true)}>
            Chat
          </Link>
        }
      </Grid>
    </Grid>
  );
}

export default Header;
