import React, { useState, useEffect } from 'react'
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { FilterMatchMode } from 'primereact/api';
import { InputText } from 'primereact/inputtext';
import { Button } from 'primereact/button';

import axios from 'axios';
import client from '../api/api';

const UserTickersTable = () => {
  const [currentUser, setCurrentUser] = useState();
  const [userTickerData, setUserTickerData] = useState();
  const [filters, setFilters] = useState({
    global: {value: null, matchMode: FilterMatchMode.CONTAINS },
  });

  useEffect(() => {
    axios.all([
      client.get("/api/user/me/"),
      client.get("/api/tunnels/tunnels/")
    ])
    .then(axios.spread((userRes, tunnelRes) => {
      setCurrentUser(userRes.data.email);
      // console.log(userRes.data);
      setUserTickerData(tunnelRes.data);
      // console.log(tunnelRes.data);
    }))
    .catch(function(error) {
      setCurrentUser(false);
    })
  }, []);

  const formatCurrency = (value) => {
    const val = parseFloat(value)
    return val.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
  };

  const lowerValBodyTemplate = (value) => {
    return formatCurrency(value.lowerVal)
  };

  const upperValBodyTemplate = (value) => {
    return formatCurrency(value.upperVal)
  };

  const header = (
    <div className="flex flex-wrap align-items-center justify-content-between gap-2">
      <span className="text-xl text-900 font-bold">Your Tickers</span>
    </div>
  );

  const footer = `In total there are ${userTickerData ? userTickerData.length : 0} tickers.`;

  if(currentUser) {
    return (
      <div className='user-table'>

        {/* Search Table */}
        <span className='p-input-icon-left'>
          <i className="pi pi-search" />
          <InputText onInput={(e) =>
            setFilters({
              global: {
                value: e.target.value,
                matchMode: FilterMatchMode.CONTAINS
              },
            })} placeholder='Search'
          />

        </span>
        <Button icon="pi pi-refresh" rounded raised />

        <DataTable value={userTickerData} header={header} footer={footer}
        paginator rows={10} rowsPerPageOptions={[5, 10, 25, 50]}
        filters={filters} tableStyle={{ minWidth: '60rem' }} >
          <Column field='id' header='ID' sortable />
          <Column field='assetId' header='Ticker' sortable />
          <Column field='lowerVal' header='Buy Value' body={lowerValBodyTemplate} sortable />
          <Column field='upperVal' header='Sell Value' body={upperValBodyTemplate} sortable />
          <Column field='interval' header='Periodicity' sortable />
        </DataTable>
      </div>
    )
  }
  return(<div>Sign in to access page.</div>)
}

export default UserTickersTable