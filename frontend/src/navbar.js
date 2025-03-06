import React from "react";
import { useNavigate } from "react-router-dom";
import "./App.css";

const Navbar = () => {
  const navigate = useNavigate();
  const token = localStorage.getItem("token");

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("client_id");
    alert("Logged out successfully!");
    navigate("/login");
  };

  return (
    <nav className="navbar">
      <h1 className="logo">Cognute AI</h1>
      <ul className="nav-links">
        <li><a href="/">Home</a></li>
        <li><a href="/#about">About</a></li>
        <li><a href="/#services">Services</a></li>
        <li><a href="/#contact">Contact Us</a></li>

        {token ? (
          // If user is logged in, show Profile & Logout
          <>
            <li><a href="/profile">Profile</a></li>
            <li>
              <button onClick={handleLogout} className="logout-button">
                Logout
              </button>
            </li>
          </>
        ) : (
          // If user is not logged in, show Signup & Login
          <>
            <li><a href="/signup">Signup</a></li>
            <li><a href="/login">Login</a></li>
          </>
        )}
      </ul>
    </nav>
  );
};

export default Navbar;
