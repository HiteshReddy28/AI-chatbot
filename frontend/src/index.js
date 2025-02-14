import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './index.css';
import App from './App';
import ChatApp from './ChatApp';
import 'bootstrap/dist/css/bootstrap.min.css';



const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Router>
      <div>
        {/* Navigation Links (Optional) */}
        

        {/* Define Routes */}
        <Routes>
          <Route path="/" element={<App />} />
          <Route path="/ChatApp" element={<ChatApp/>} />
        </Routes>
      </div>
    </Router>
  </React.StrictMode>
);


