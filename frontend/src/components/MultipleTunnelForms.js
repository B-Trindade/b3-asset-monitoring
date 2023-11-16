import React from 'react';

import NewTunnelForm from './NewTunnelForm';

const MultipleTunnelForms = ({tickerList}) => {
  const tickers = tickerList
  const litsTunnels = tickers.map(
    ticker => <NewTunnelForm ticker={ticker} />
  );

  return (<div>{litsTunnels}</div>)
}

export default MultipleTunnelForms