import React from 'react';

import Form from 'react-bootstrap/Form';
import InputGroup from 'react-bootstrap/InputGroup';

const NewTunnelForm = ({ticker}) => {
  return (
    <>
      <Form.Label>{ticker}</Form.Label>
      <InputGroup className="mb-3">
        <InputGroup.Text>Lower Threshold</InputGroup.Text>
        <Form.Control aria-label="Lower Threshold" type='number'/>
        <InputGroup.Text>Upper Threshold</InputGroup.Text>
        <Form.Control aria-label="Upper Threshold" type='number'/>
      </InputGroup>
    </>
  )
}

export default NewTunnelForm