import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./login.css";

const Loginform = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setUser({ ...user, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
        const response = await fetch("http://localhost:8000/api/token", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: new URLSearchParams({
                username: user.email,
                password: user.password,
            }),
        });

        const result = await response.json();

        if (response.ok) {
            localStorage.setItem("token", result.access_token);

            
            const userInfoResponse = await fetch(`http://localhost:8000/api/userinfo`, {
                method: "GET",
                headers: { "Authorization": `Bearer ${result.access_token}` },
            });

            if (userInfoResponse.ok) {
                const userInfo = await userInfoResponse.json();
                console.log("Fetched client_id:", userInfo.client_id);  
                localStorage.setItem("client_id", userInfo.client_id);
            } else {
                console.error("Failed to fetch client ID");
            }

            alert("Login successful!");
            navigate("/ChatApp");  
        } else {
            setError(result.detail || "Invalid credentials.");
        }
    } catch (err) {
        setError("Login failed. Please try again.");
    }
};




  return (
    <div className="login-form">
      <h2>Login</h2>
      {error && <p className="error">{error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Email:</label>
          <input
            type="email"
            name="email"
            value={user.email}
            onChange={handleChange}
            required
          />
        </div>

        <div>
          <label>Password:</label>
          <input
            type="password"
            name="password"
            value={user.password}
            onChange={handleChange}
            required
          />
        </div>
        <br />
        <button type="submit" disabled={loading}>
          {loading ? "Logging in..." : "Login"}
        </button>
      </form>
    </div>
  );
};

export default Loginform;


