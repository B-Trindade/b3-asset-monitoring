import axios from 'axios';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;
axios.defaults.withXSRFToken = (config) => !!config.useCredentials;

const client = axios.create({
  // baseURL: "http://127.0.0.1:8000",
  withCredentials: true
});

export default client;