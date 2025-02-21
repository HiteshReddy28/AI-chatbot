import React from "react";
import "./App.css";
import { Link } from "react-router-dom";


const Navbar = () => {
  return (
    <nav className="navbar">
      <h1 className="logo">Cognute AI</h1>
      <ul className="nav-links">
        <li><a href="#home">Home</a></li>
        <li><a href="#about">About</a></li>
        <li><a href="#services">Services</a></li>
        <li><a href="#contact">Contact Us</a></li>
        <li>
          <Link to="/signup" className="signup-btn">
            Sign Up
          </Link>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;
