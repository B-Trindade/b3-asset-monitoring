import React from 'react'
import { useState, useEffect } from 'react';

import client from '../api/api';

import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

const LoginPage = () => {
    const [currentUser, setCurrentUser] = useState();
    const [registrationToggle, setRegistrationToggle] = useState(false);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [name, setName] = useState('');

    useEffect(() => {
      client.get("/api/user/me/")
      .then(function(res) {
        setCurrentUser(true);
      })
      .catch(function(error) {
        setCurrentUser(false);
      })
    }, []);

    function update_form_btn() {
      if (registrationToggle) {
        document.getElementById("form_btn").innerHTML = "Register";
        setRegistrationToggle(false);
      } else {
        document.getElementById("form_btn").innerHTML = "Sign in";
        setRegistrationToggle(true);
      }
    }

    function submitRegistration(e) {
      e.preventDefault();
      client.post(
        "/api/user/create/",
        {
          email: email,
          password: password,
          name: name
        }
      ).then(function(res) {
        client.post(
          "/api/user/login/",
          {
            email: email,
            password: password
          }
        ).then(function(res) {
          setCurrentUser(true);
        });
      });
    }

    function submitLogin(e) {
      e.preventDefault();
      client.post(
        "api/user/login/",
        {
          email: email,
          password: password
        }
      ).then(function(res) {
        setCurrentUser(true);
      });
    }

    function submitLogout(e) {
      e.preventDefault();
      client.post(
        "/api/user/logout/",
        {withCredentials: true}
      ).then(function(res) {
        setCurrentUser(false);
      });
    }

    if (currentUser) {
      return (
        <div>
          <Navbar collapseOnSelect expand="lg" className="bg-body-tertiary">
            <Container>
              <Navbar.Brand href="#home">B3 Notify</Navbar.Brand>
              <Navbar.Toggle aria-controls="responsive-navbar-nav" />
              <Navbar.Collapse id="responsive-navbar-nav">
                <Nav className="me-auto">
                  <Nav.Link href="#features">Home</Nav.Link>
                  <Nav.Link href="#pricing">Add Tickers</Nav.Link>
                </Nav>
                <Navbar.Text>
                  <form onSubmit={e => submitLogout(e)}>
                    <Button type='submit' variant='dark'>Sign out</Button>
                  </form>
                </Navbar.Text>
                {/* <Nav>
                  <Nav.Link eventKey={2} href="#memes">
                    Sign out
                  </Nav.Link>
                </Nav> */}
              </Navbar.Collapse>
            </Container>
          </Navbar>
          <div className='center'>
            <h2>You're logged in!</h2>
          </div>
        </div>
      );
    }
    return (
      <div>
      <Navbar collapseOnSelect expand="lg" className="bg-body-tertiary">
        <Container>
          <Navbar.Brand href="#home">B3 Notify</Navbar.Brand>
          <Navbar.Toggle aria-controls="responsive-navbar-nav" />
          <Navbar.Collapse id="responsive-navbar-nav">
            <Nav className="me-auto">
              <Nav.Link href="#features">Home</Nav.Link>
              <Nav.Link href="#pricing">Add Tickers</Nav.Link>
            </Nav>
            <Navbar.Text>
              <Button id='form_btn' onClick={update_form_btn}
                variant='dark'>Register</Button>
            </Navbar.Text>
            {/* <Nav>
              <Nav.Link eventKey={2} href="#memes">
                Sign out
              </Nav.Link>
            </Nav> */}
          </Navbar.Collapse>
        </Container>
      </Navbar>
      {
        registrationToggle ? (
          <div className='center'>
            <Form onSubmit={e => submitRegistration(e)}>
              <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Label>Email address</Form.Label>
                <Form.Control type="email" placeholder="Enter email"
                  value={email} onChange={e => setEmail(e.target.value)}/>
                <Form.Text className="text-muted">
                  We'll never share your email with anyone else.
                </Form.Text>
              </Form.Group>

              <Form.Group className='mb-3' controlId='formBasicName'>
                <Form.Label>Name</Form.Label>
                <Form.Control type='text' placeholder='Enter full name'
                  value={name} onChange={e => setName(e.target.value)} />
              </Form.Group>

              <Form.Group className="mb-3" controlId="formBasicPassword">
                <Form.Label>Password</Form.Label>
                <Form.Control type="password" placeholder="Password"
                  value={password} onChange={e => setPassword(e.target.value)} />
              </Form.Group>
              {/* <Form.Group className="mb-3" controlId="formBasicCheckbox">
                <Form.Check type="checkbox" label="Check me out" />
              </Form.Group> */}
              <Button variant="primary" type="submit">
                Submit
              </Button>
            </Form>
          </div>
        ) : (
          <div className='center'>
            <Form onSubmit={e => submitLogin(e)}>
              <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Label>Email address</Form.Label>
                <Form.Control type="email" placeholder="Enter email"
                  value={email} onChange={e => setEmail(e.target.value)}/>
                <Form.Text className="text-muted">
                  We'll never share your email with anyone else.
                </Form.Text>
              </Form.Group>

              <Form.Group className="mb-3" controlId="formBasicPassword">
                <Form.Label>Password</Form.Label>
                <Form.Control type="password" placeholder="Password"
                  value={password} onChange={e => setPassword(e.target.value)} />
              </Form.Group>
              {/* <Form.Group className="mb-3" controlId="formBasicCheckbox">
                <Form.Check type="checkbox" label="Check me out" />
              </Form.Group> */}
              <Button variant="primary" type="submit">
                Submit
              </Button>
            </Form>
          </div>
        )
      }
      </div>
    );
}

export default LoginPage