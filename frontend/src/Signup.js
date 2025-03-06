import React, { useState } from "react";
import { FcGoogle } from "react-icons/fc";
import { FaApple } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import "./Signup.css";
import Navbar from './navbar.js';
import Footer from './footer.js';


const Signup = () => {
  console.log("Signup Component is Rendering"); // Debugging log

  const navigate = useNavigate();
  const [user, setUser] = useState({
    first_name: "", // Ensure correct field names
    last_name: "",
    email: "",
    password: "",
    ssn: "123-45-6789", // Temporary placeholder
    loan_amount: 5000.00, // Temporary placeholder
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
      const response = await fetch("http://localhost:8000/api/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          first_name: user.first_name, // Fix naming
          last_name: user.last_name,   // Fix naming
          email: user.email,
          password: user.password,
          ssn: user.ssn,
          loan_amount: user.loan_amount
        }),
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem("client_id", data.client_id);
        alert(`Signup successful! Your Client ID: ${data.client_id}`);
        navigate("/login");
      } else {
        setError(data.detail || "Signup failed.");
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
                  name="first_name"
                  placeholder="First Name"
                  value={user.first_name}
                  onChange={handleChange}
                  required
                />
                <input
                  type="text"
                  name="last_name"
                  placeholder="Last Name"
                  value={user.last_name}
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
              <input
                type="text"
                name="ssn"
                placeholder="SSN (e.g., 123-45-6789)"
                value={user.ssn}
                onChange={handleChange}
                required
              />
              <input
                type="number"
                name="loan_amount"
                placeholder="Loan Amount"
                value={user.loan_amount}
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
      <Footer />
    </>
  );
};

export default Signup;
