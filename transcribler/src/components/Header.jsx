
import {useState} from 'react';
import { NavLink } from 'react-router-dom';

import Button from '@mui/material/Button';

function Header() {
  const [isSummary, setIsSummary] = useState(true);
  return (
    <div>
      <Button component={NavLink} to='/history' className="navlink">
        History
      </Button>
      <Button component={NavLink} to='/'>
        <img src="/imgs/Logo1_35x103.png" alt="img"/>
      </Button>
      {isSummary ? 
        <Button component={NavLink} to='/summary' className="navlink" onClick={()=>setIsSummary(false)}>
          Summary
        </Button>
        :
        <Button component={NavLink} to='/chat' className="navlink" onClick={()=>setIsSummary(true)}>
          Chat
        </Button>
      }
    </div>
  );
}

export default Header;
