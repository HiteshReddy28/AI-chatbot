// login.js
import React, { useState } from 'react';
import './login.css';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const messages = [
    'Provides 24/7 assistance and personalized customer service',
    'Another sentence to show on the second dot',
    'A third sentence for the third dot'
  ];

  // 2) Active message index
  const [activeIndex, setActiveIndex] = useState(0);


  const handleGoogleLogin = () => {
    alert('Google login clicked');
  };

  const handleAppleLogin = () => {
    alert('Apple login clicked');
  };

  const handleLogin = (e) => {
    e.preventDefault();
    alert(`Email: ${email}\nPassword: ${password}`);
  };

  return (
    <div className="login-container">
      {/* Left Section: Gradient background, Robot image, and text */}
      <div className="left-section">
        <img
          src="/Bot.png" 
          alt="Robot"
          className="robot-image"
        />
        <div className="shadow-ellipse"></div>
        <p className="left-subtitle">

          {messages[activeIndex]}
        </p>

      {/* Three dots to switch messages */}
      <div className="dots">
        {messages.map((_, i) => (
        <span
        key={i}
        className={`dot ${i === activeIndex ? 'active' : ''}`}
        onClick={() => setActiveIndex(i)}
      />
      ))}
      </div>
    </div>   

      {/* Right Section: White background with the login form */}
      <div className="right-section">
      <h1 className="brand-title">
        Ai Negotiator<span className="brand-dot">.</span>
      </h1>
        <h2 className="right-heading">Log into your Account</h2>
        <p className="right-subtitle">
          Welcome back! Select a method to log in:
        </p>

        {/* Social login buttons */}
        <div className="social-login-container">
          <button className="social-button" onClick={handleGoogleLogin}>
          <img src="/google_.png" alt="Google logo" className="social-logo" />
            Google
          </button>
          <button className="social-button" onClick={handleAppleLogin}>
          <img src="/apple.png" alt="Apple logo" className="social-logo" />
            Apple
          </button>
        </div>
        <div className="or-text">or continue with email</div>

        {/* Login form */}
        <form onSubmit={handleLogin} className="login-form">
          <label className="login-label" htmlFor="email">
            Email
          </label>
          <input
            id="email"
            type="email"
            className="login-input"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <label className="login-label" htmlFor="password">
            Password
          </label>
          <input
            id="password"
            type="password"
            className="login-input"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <div className="remember-forgot-container">
            <div>
              <input type="checkbox" id="rememberMe" />
              <label htmlFor="rememberMe" className="remember-me-label">
                Remember me
              </label>
            </div>
            <a href="#!" className="forgot-link">
              Forgot Password
            </a>
          </div>

          <button type="submit" className="login-button">
            Log In
          </button>
        </form>
      </div>
    </div>
  );
}

export default Login;
