import Loginform from "./Loginpage";
import "./login.css"
import Footer from "./footer";
import Navbar from "./navbar";

function Login(){
    return(
        <>
        <Navbar/>
        <div className="login-container">
            
            <div className="login-left">
                <img src="/Bot.png" alt="bot"></img>
                <p> Provides 24/7 assistance and personalized customer service</p>
            </div>
            <div className="login-right">
                <Loginform/>
            </div>
        </div>
        <Footer/>
        </>
    );
}

export default Login;