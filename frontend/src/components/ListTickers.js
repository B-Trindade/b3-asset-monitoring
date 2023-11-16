import React from 'react'
import { useState } from 'react';

import { MultiSelect } from 'primereact/multiselect';
import { Button } from 'primereact/button';
import { useNavigate } from 'react-router-dom';

import client from '../api/api';


const ListTickers = () => {

  const [selectedTickers, setSelectedTickers] = useState([]);
  const [tickers, setTickers] = useState(() => getTickers());
  const navigate = useNavigate();

  function getTickers() {
    // client.get(
    //   "/api/asset/list/",
    //   {withCredentials: true}
    // )
    client.get("https://jsonplaceholder.typicode.com/users")
    .then(response => setTickers(response.data))
  }

  // Sends selected tickers as props for the Add Tunnel page.
  function submitTickers() {
    navigate('/add-tunnel', {selectedTickers});
    // console.log(selectedTickers)
  }

  return (
    <div>
      <MultiSelect
        value={selectedTickers}
        onChange={(e) => setSelectedTickers(e.value)}
        options={tickers} optionLabel="name" //change to "symbol"
        display="chip"
        placeholder="Select Tickers"
        maxSelectedLabels={3}
        className="w-full md:w-20rem"
        filter={true}
      />
      <br/>
      <Button type='submit' label='Submit' onClick={submitTickers}/>
    </div>
  )
}

export default ListTickers