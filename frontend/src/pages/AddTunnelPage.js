import React from 'react';
import { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';

import client from '../api/api';

import CustomNavbar from '../components/CustomNavbar';
import NewTunnelForm from '../components/MultipleTunnelForms';

import Button from 'react-bootstrap/esm/Button';


const AddTunnelPage = () => {
  const [userTickers, setUserTickers] = useState([]);
  const [currentUser, setCurrentUser] = useState();
  const location = useLocation();

  useEffect(() => {
    client.get("/api/user/me/")
    .then(function(res) {
      setCurrentUser(true);
      setUserTickers(location.state.symbols);
    })
    .catch(function(error) {
      setCurrentUser(false);
    })
  }, []);

  if(currentUser){
    return (
      <div>
        <CustomNavbar />
        <div className='tunnel-form'>
          <NewTunnelForm tickerList={userTickers} />
          <br/>
          <Button variant='primary'>Submit</Button>
        </div>
      </div>
    )
  }
  return(<div>Not logged in</div>)
}

export default AddTunnelPage