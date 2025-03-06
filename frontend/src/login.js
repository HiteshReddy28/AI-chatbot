import React from "react";
import Loginform from "./Loginpage.js";  
import Navbar from "./navbar.js";        
import Footer from "./footer.js";        
import "./login.css";

function Login() {
    return (
        <>
            <Navbar />
            <div className="login-container">
                <div className="login-left">
                    <img src="/Bot.png" alt="Chatbot" />
                    <p>Provides 24/7 assistance and personalized customer service</p>
                </div>
                <div className="login-right">
                    <Loginform />
                </div>
            </div>
            <Footer />
        </>
    );
}

export default Login;
