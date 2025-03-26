import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './index.css';
import App from './App';
import ChatApp from './ChatApp';
import Login from './login';
import Signup from './Signup';
import 'bootstrap/dist/css/bootstrap.min.css';
import ChatInterface from './chatinterface';
import ChatInput from './chatinput';
import Test from './ApiTest';


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Router>
      <div>
        <Routes>
          {/* <Route path="/" element={<Test/>} /> */}
          <Route path="/ChatApp" element={< ChatInterface />} />
          <Route path="/login" element ={<Login/>}/>
          <Route path="/Signup" element={<Signup />} />
        </Routes>
      </div>
    </Router>
  </React.StrictMode>
);


