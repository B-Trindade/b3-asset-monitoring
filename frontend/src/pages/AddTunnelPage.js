import React from 'react';
import { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

import client from '../api/api';
import axios from 'axios';

import CustomNavbar from '../components/CustomNavbar';
import NewTunnelForm from '../components/NewTunnelForm';
import Button from 'react-bootstrap/esm/Button';
import Form from 'react-bootstrap/Form';


const AddTunnelPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [currentUser, setCurrentUser] = useState();
  const [userTickers, setUserTickers] = useState([]);
  const [tunnelData, setTunnelData] = useState([]);

  useEffect(() => {
    client.get("/api/user/me/")
    .then(function(res) {
      setCurrentUser(res.data.email);
      setUserTickers(location.state.symbols);
      initializeForm();
    })
    .catch(function(error) {
      setCurrentUser(false);
    })
  }, [currentUser, location.state.symbols]);

  // Creates a json response for each asset selected
  // and initializes its values accordingly.
  function initializeForm() {
    userTickers.forEach(tickerName => {
      setTunnelData(currentTunnelData => [
        ...currentTunnelData,
        {
          userId: currentUser,
          assetId: tickerName,
          lowerVal: '',
          upperVal: '',
          interval: '',
        }
      ])
    })
  }

  function submitTunnel(e) {
    e.preventDefault();
    // console.log(tunnelData);
    const postRequests = tunnelData.map(
      (tunnel) => {
        client.post(
          "/api/tunnels/tunnels/",
          tunnel,
          {withCredentials: true,
          withXSRFToken: true},
        )
        // console.log(tunnel)
      }
    );
    axios.all(postRequests)
    .then((responses) => {
      responses.forEach((res) => {
        console.log(res);
        // let msg = {
        //   // server: res.headers.server,
        //   status: res.status,
        //   fields: Object.keys(res.data).toString(),
        // };
        // console.info(res.config.url);
        // console.table(msg);
      });
    })
    .then(navigate('/home/'));
  }

  if(currentUser){
    return (
      <div>
        <CustomNavbar />
        <div className='tunnel-form-container'>
          <Form className='tunnel-form' onSubmit={submitTunnel}>
            {
              userTickers.map((ticker, index) => {
                return(
                  <NewTunnelForm
                    key={index}
                    index={index}
                    ticker={ticker}
                    formData={tunnelData}
                    setFormData={setTunnelData}
                  />
                )
              })
            }
            <br/>
            <Button className='submit-button' variant='primary'
              type='submit' value='Submit'>Submit</Button>
            {/* <div>
            {JSON.stringify(tunnelData, null, 2)}
            </div> */}
          </Form>
        </div>
      </div>
    )
  }
  return(<div>Not logged in</div>)
}

export default AddTunnelPage