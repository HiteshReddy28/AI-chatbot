import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './index.css';
import App from './App';
import Login from './login';
import 'bootstrap/dist/css/bootstrap.min.css';
import ChatInterface from './chatinterface';
import Signup from './Signup';
import ChatBot from './Chatbot';
import ClientProfile from "./clientprofile";

console.log("React Router Loaded");  

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/ChatApp" element={<ChatInterface />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/Chatbot" element={<ChatBot />} />
        <Route path="/profile" element={<ClientProfile />} />
      </Routes>
    </Router>
  </React.StrictMode>
);
