import React from 'react'
import { useState, useEffect } from 'react';

import client from '../api/api';

import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Button from 'react-bootstrap/Button';
import { useNavigate, Link } from 'react-router-dom'

const CustomNavbar = () => {
  const [currentUser, setCurrentUser] = useState();
  const navigate = useNavigate();

  useEffect(() => {
    client.get("/api/user/me/")
    .then(function(res) {
      setCurrentUser(true);
    })
    .catch(function(error) {
      setCurrentUser(false);
    })
  }, []);

  function submitLogout(e) {
    e.preventDefault();
    client.post(
      "/api/user/logout/",
      {withCredentials: true}
    ).then(function(res) {
      setCurrentUser(false);
      navigate('/');
    });
  }

  if(currentUser) {
    return (
      <Navbar collapseOnSelect expand="lg" className="bg-body-tertiary">
        <Container>
          <Navbar.Brand as={Link} to="/home/">B3 Notify</Navbar.Brand>
          <Navbar.Toggle aria-controls="responsive-navbar-nav" />
          <Navbar.Collapse id="responsive-navbar-nav">
            <Nav className="me-auto">
              <Nav.Link as={Link} to="/home/" replace={true}>Home</Nav.Link>
              <Nav.Link as={Link} to="/selectTickers/">Add Tickers</Nav.Link>
            </Nav>
            <Navbar.Text>
              <form onSubmit={e => submitLogout(e)}>
              <Button type='submit' variant='dark'>Sign out</Button>
              </form>
            </Navbar.Text>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    );
  }
  return (
    <Navbar collapseOnSelect expand="lg" className="bg-body-tertiary">
      <Container>
        <Navbar.Brand href="/home">B3 Notify</Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="me-auto">
            {/* <Nav.Link as={Link} to="/home/" replace={true}>Home</Nav.Link>
            <Nav.Link as={Link} to="/selectTickers/">Add Tickers</Nav.Link> */}
          </Nav>
          <Navbar.Text>
            <Button id='form_btn' // onClick={update_form_btn}
              variant='dark'>Login</Button>
          </Navbar.Text>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default CustomNavbar