import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './index.css';
import App from './App';
import Login from './login';
import 'bootstrap/dist/css/bootstrap.min.css';
import ChatInterface from './chatinterface';
import Signup from './Signup';
import ChatBot from './Chatbot';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<App/>} />
          <Route path="/ChatApp" element={< ChatInterface />} />
          <Route path="/login" element ={<Login/>}/>
          <Route path = "/Signup" element={<Signup/>}/>
          <Route path="/Chatbot" element={<ChatBot/>}/>
        </Routes>
      </div>
    </Router>
  </React.StrictMode>
);


