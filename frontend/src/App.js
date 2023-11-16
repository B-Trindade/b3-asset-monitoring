import './App.css';
import "primereact/resources/themes/bootstrap4-light-blue/theme.css";

import {
  BrowserRouter as Router,
  Routes,
  Route
} from "react-router-dom";


import { PrimeReactProvider } from 'primereact/api';

import LoginPage from './pages/LoginPage';
import TickerSelectionPage from './pages/TickerSelectionPage';

function App() {
  return (
    <PrimeReactProvider>
      <Router>
        <div className='App'>
          <Routes>
              <Route path='/' exact element={<LoginPage/>} />
              <Route path='/selectTickers/' exact element={<TickerSelectionPage/>} />
          </Routes>
        </div>
      </Router>
    </PrimeReactProvider>
  );
}

export default App;
