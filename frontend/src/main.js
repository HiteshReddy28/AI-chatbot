import { useNavigate } from 'react-router-dom';
import "./App.css";
import { motion } from "framer-motion";
import Footer from './footer';
import Navbar from './navbar';


function Mainpage(){
    const navigate = useNavigate();
    function handleClick(){
        navigate('/ChatApp')
    }
    return (
        <>
          <section className="hero">
            <div className="hero-content">
                <motion.h1 initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 1.5, ease: "easeInOut" }}>
                    <h1 className="hero-head"><span className='Design'>Revolutionize</span> Customer Service with Chatbot</h1>
                </motion.h1>
                <p>Say goodbye to long wait times and frustrating interactions. Our chatbot robots provide 24/7 assistance and personalized service for our customers.</p>
                <button className="cta-button" onClick={handleClick}>Get Started</button>
            </div>
            <div className="hero-image">
                <img src='/Bot.png' alt="Chatbot" />
                    <div className="footer" style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px'}}>
                        <p className='para'>Cookie Policy</p>
                        <p className='para'>2025 Cognute, All Rights Reserved</p>
                    </div>
            </div>
            </section>
        </>

    );
}

export default Mainpage;