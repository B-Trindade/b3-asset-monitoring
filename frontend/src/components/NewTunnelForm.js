// REST API "/api/tunnels/tunnel/" endpoint expects
// POST form data as:
//
// {
//   "userId": "user@example.com",
//   "assetId": "SYMBOL.NAME",
//   "lowerVal": 0.00,
//   "upperVal": 0.00,
//   "interval": 0
// }
//
// Check "/api/docs/" endpoint for more details.
// ########################################################

import React from 'react';

import Form from 'react-bootstrap/Form';
import InputGroup from 'react-bootstrap/InputGroup';

const NewTunnelForm = ({ticker, index, formData, setFormData}) => {

  function handleChange(index, field, value) {
    const updatedFormData = [...formData];
    updatedFormData[index][field] = value;
    setFormData(updatedFormData);
  }

  return (
    <>
      <Form.Label>{ticker}</Form.Label>
      <InputGroup className="mb-3">
        <InputGroup.Text>Lower Threshold</InputGroup.Text>
        <Form.Control
          aria-label="Lower Threshold"
          placeholder='0.00'
          type='number'
          onChange={e => handleChange(index, 'lowerVal', e.target.value)}
        />
        <InputGroup.Text>Upper Threshold</InputGroup.Text>
        <Form.Control
          aria-label="Upper Threshold"
          placeholder='0.00'
          type='number'
          onChange={e => handleChange(index, 'upperVal', e.target.value)}
        />
        <br/>
        <InputGroup.Text>Periodicity</InputGroup.Text>
        <Form.Control
          aria-label='Periodicity'
          type='number'
          max={720}
          onChange={e => handleChange(index, 'interval', parseInt(e.target.value))}
        />
      </InputGroup>
    </>
  )
}

export default NewTunnelForm