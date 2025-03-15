import React, { useState } from "react";
import { FcGoogle } from "react-icons/fc";
import { FaApple } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./Signup.css";  
import Navbar from './navbar';
import Footer from './footer';


const Signup = () => {
  console.log("Signup Component is Rendering");  // Debugging log

  const navigate = useNavigate();
  const [user, setUser] = useState({
    firstName: "",
    lastName: "",
    email: "",
    password: "",
    agree: false
  });

  const [error, setError] = useState("");

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setUser({ ...user, [name]: type === "checkbox" ? checked : value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!user.agree) {
      setError("You must agree to the Terms and Conditions.");
      return;
    }
    setError("");

    try {
      const response = await axios.post("http://localhost:3000/signup", user);
      if (response.data.success) {
        navigate("/login");
      } else {
        setError(response.data.message);
      }
    } catch (error) {
      setError("Signup failed. Please try again.");
    }
  };

  return (
    <>
      <Navbar /> 
    <div className="signup-container">
      {/* Left Side - Chatbot Image */}
      <div className="signup-left">
        <img src='/Bot.png' alt="Chatbot" className="robot-img" />
        <p>Provides 24/7 assistance and personalized customer service</p>
      </div>

      {/* Right Side - Signup Form */}
      <div className="signup-right">
        <div className="signup-form">
          <h2 className="brand-title">Ai <span className="highlight-dot">Negotiator</span><span className="dot">.</span></h2>
          <h3 className="signup-heading">Create an Account</h3>
          <p className="text-sm">
            Already have an account? <a href="/login" className="login-link">Log in</a>
          </p>

          {error && <p className="error">{error}</p>}

          <form onSubmit={handleSubmit}>
            <div className="name-inputs">
              <input
                type="text"
                name="firstName"
                placeholder="First Name"
                value={user.firstName}
                onChange={handleChange}
                required
              />
              <input
                type="text"
                name="lastName"
                placeholder="Last Name"
                value={user.lastName}
                onChange={handleChange}
                required
              />
            </div>
            <input
              type="email"
              name="email"
              placeholder="Email"
              value={user.email}
              onChange={handleChange}
              required
            />
            <input
              type="password"
              name="password"
              placeholder="Enter your password"
              value={user.password}
              onChange={handleChange}
              required
            />

            <div className="checkbox-container">
              <input
                type="checkbox"
                name="agree"
                checked={user.agree}
                onChange={handleChange}
              />
              <label>
                I agree to the <a href="#">Terms and Conditions</a>
              </label>
            </div>

            <button type="submit" className="signup-button">Create Account</button>
          </form>

          {/* Divider */}
          <div className="divider">
            <hr className="line" />
            <p className="divider-text">or register with</p>
            <hr className="line" />
          </div>

          {/* Social Signup */}
          <div className="social-signup">
            <button className="social-btn">
              <FcGoogle className="icon" />
              Google
            </button>
            <button className="social-btn">
              <FaApple className="icon" />
              Apple
            </button>
          </div>
        </div>
      </div>
    </div>
    <Footer/>
  </>
  );
};

export default Signup;