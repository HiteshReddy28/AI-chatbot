import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './index.css';
import App from './App';
import ChatApp from './ChatApp';
import Login from './login';
import 'bootstrap/dist/css/bootstrap.min.css';
import ChatInterface from './chatinterface';
import ChatInput from './chatinput';


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<App/>} />
          <Route path="/ChatApp" element={< ChatInterface />} />
          <Route path="/login" element ={<Login/>}/>
        </Routes>
      </div>
    </Router>
  </React.StrictMode>
);


