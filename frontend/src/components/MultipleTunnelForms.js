import React from 'react';

import NewTunnelForm from './NewTunnelForm';

const MultipleTunnelForms = ({tickerList, onChange}) => {
  const tickers = tickerList
  const litsTunnels = tickers.map(
    ticker => <NewTunnelForm
      ticker={ticker} key={ticker}
      onChange={onChange}
    />
  );

  return (<div>{litsTunnels}</div>)
}

export default MultipleTunnelForms