import Navbar from "./navbar";
import ChatApp from "./ChatApp";
import { useNavigate } from 'react-router-dom';
import "./App.css";


function Mainpage(){
    const navigate = useNavigate();
    function handleClick(){
        navigate('/ChatApp')
    }
    return (
        <>

<section className="hero">
      <div className="hero-content">
        <h1>Revolutionize Customer Service with Chatbot</h1>
        <p>Say goodbye to long wait times and frustrating interactions. Our chatbot robots provide 24/7 assistance and personalized service for our customers.</p>
        <button className="cta-button" onClick={handleClick}>Get Started &gt;</button>
      </div>
      <div className="hero-image">
        {/* <img src={chatbotImage} alt="Chatbot" /> */}
      </div>
    </section>
        </>

    );
}

export default Mainpage;