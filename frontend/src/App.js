import './App.css';

import {
  BrowserRouter as Router,
  Routes,
  Route
} from "react-router-dom";

import LoginPage from './pages/LoginPage';
import CustomNavbar from './components/CustomNavbar';

function App() {
  return (
    <Router>
      <div className='App'>
        <Routes>
            <Route path='/' exact element={<LoginPage/>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
