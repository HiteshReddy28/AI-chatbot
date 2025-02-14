import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import ChatApp from './ChatApp';
import 'bootstrap/dist/css/bootstrap.min.css';
import ChatInterface from './chatinterface';


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <ChatInterface/>
  </React.StrictMode>
);


