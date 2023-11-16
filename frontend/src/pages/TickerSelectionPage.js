import React from 'react';
import { useState, useEffect } from 'react';
import { MultiSelect } from 'primereact/multiselect';

import client from '../api/api';

import CustomNavbar from '../components/CustomNavbar';
import ListTickers from '../components/ListTickers';

const TickerSelectionPage = () => {

  const [currentUser, setCurrentUser] = useState();

  useEffect(() => {
    client.get("/api/user/me/")
    .then(function(res) {
      setCurrentUser(true);
    })
    .catch(function(error) {
      setCurrentUser(false);
    })
  }, []);

  if (currentUser) {
    return (
      <div>
        <CustomNavbar />
        <div className='ticker-list'>
          <ListTickers />
        </div>
      </div>
    );
  }
  return(<div><h1>Sign in.</h1></div>);
}

export default TickerSelectionPage