import React from "react";
import "./App.css";

const Footer = () => {
  return (
    <footer className="footer" style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px'}}>
      <p >Cookie Policy</p>
      <p>2025 Cognute, All Rights Reserved</p>
    </footer>
  );
};

export default Footer;
