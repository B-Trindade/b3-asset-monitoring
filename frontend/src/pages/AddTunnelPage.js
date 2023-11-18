import React from 'react';
import { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';

import client from '../api/api';

import CustomNavbar from '../components/CustomNavbar';
import MultipleTunnelForms from '../components/MultipleTunnelForms';

import Button from 'react-bootstrap/esm/Button';
import Form from 'react-bootstrap/Form';


const AddTunnelPage = () => {
  const [tunnels, setTunnels] = useState([]);
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

  function submitTunnel(e) {
    e.preventDefault();
    // client.postForm
  }

  if(currentUser){
    return (
      <div>
        <CustomNavbar />
        <div className='tunnel-form-container'>
          <Form className='tunnel-form' onSubmit={submitTunnel}>
            <MultipleTunnelForms tickerList={userTickers}
            onChange={() => setTunnels}/>
            <br/>
            <Button className='submit-button' variant='primary'
              type='submit' value='Submit'>Submit</Button>
          </Form>
        </div>
      </div>
    )
  }
  return(<div>Not logged in</div>)
}

export default AddTunnelPage