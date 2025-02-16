import Loginform from "./Loginpage";
import "./login.css"
import Navbar from "./navbar";

function Login(){
    return(
        <>
        <Navbar/>
        <div className="login-container">
            
            <div className="login-left">
                <img src="bot.png" alt="bot"></img>
                <p> Provides 24/7 assistance and personalized customer service</p>
            </div>
            <div className="login-right">
                <Loginform/>
            </div>
        </div>
        </>
    );
}

export default Login;