import React, { useState } from 'react';
import { Settings, RefreshCw, ArrowLeft, Send, Paperclip, Image } from 'lucide-react';
import { Navigate, useNavigate } from 'react-router-dom';
import './Chatapp.css'
import Signup from './Signup';


const ChatInterface = () => {
  const [inputMessage, setInputMessage] = useState('');
  const [messages, setMessages] = useState([]);
  const [showPrompts, setShowPrompts] = useState(true);
  
  
  const navigate = useNavigate();
    function onBackClick(){
        navigate('/');
    }
    
    function handleClick(){
        navigate("/Signup");
    }

    function loginClick(){
      navigate('/Login');
    }
  

  const commonPrompts = [
    'Can I refinance my existing loan?',
    'Does applying for a loan impact my credit score?',
    'How is my financial risk assessed for a loan?',
    'What are Debt-to-Income (DTI)?'
  ];
  const callOllamaAPI = async (prompt) => {
    const response = await fetch('http://localhost:8000/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ "prompt":prompt, "session_id": "123" }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;

  };

  const handleSendMessage = async () => {
    
    if (inputMessage.trim()) {
      try {
        const userMessage = {
          text: inputMessage,
          sender: 'user',
          timestamp: new Date().toLocaleTimeString(),
        };
  
        setMessages(prev => [...prev, userMessage]);
        setInputMessage('');
        setShowPrompts(false);
  
        const response = await callOllamaAPI(inputMessage);
        const botMessage = {
          text: response.message,
          sender: 'bot',
          timestamp: new Date().toLocaleTimeString(),
        };
  
        setMessages(prev => [...prev, botMessage]);
      } catch (error) {
        console.error('Error:', error);
        const errorMessage = {
          text: 'Sorry, I encountered an error. Please try again.',
          sender: 'bot',
          timestamp: new Date().toLocaleTimeString(),
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    }
  };

  return (
    <div className="chat-container">
      <div className="sidebar">
        <div className="sidebar-content">
          <div className="sidebar-header">
            <ArrowLeft 
              className="back-button" 
              onClick={onBackClick} 
            />
            <h1 className="app-title">AI Negotiator.</h1>
          </div>

          <div className="auth-buttons">
            <button className="login-btn" onClick={loginClick}>
              Login
            </button>
            <button className="signup-btn" onClick={handleClick}>
              Sign Up
            </button>
            <p className="auth-note">Sign-in to save your conversation</p>
          </div>

          <div className="history-button">
            <RefreshCw className="history-icon" />
            <span>Previous History</span>
          </div>

          <div className="settings-button">
            <Settings className="settings-icon" />
            <span>Settings</span>
          </div>
        </div>
      </div>
      
      <div className="main-content">
        <div className="chat-wrapper">
          {showPrompts ? (
            <>
              <div className="prompt-header">
                <h2>Hi there,</h2>
                <h3>What would you like to know?</h3>
                <p className="prompt-subtext">
                  Start with one of most common prompts below or use your own to begin
                </p>
              </div>

              <div className="prompt-grid">
                {commonPrompts.map((prompt, index) => (
                  <button
                    key={index}
                    className="prompt-button"
                    onClick={() => setInputMessage(prompt)}
                  >
                    {prompt}
                  </button>
                ))}
              </div>

              <div className="refresh-prompts">
                <RefreshCw className="refresh-icon" />
                <span>Refresh Prompts</span>
              </div>
            </>
          ) : (
            <div className="message-container">
              

              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`message-row ${message.sender === 'user' ? 'user' : 'bot'}`}
                >
                  <div className={`message-bubble ${message.sender === 'user' ? 'user-message' : 'bot-message'}`}>
                    <p>{message.text}</p>
                    <span className="message-time">
                      {message.timestamp}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}

          <div className="input-container">
            <div className="input-wrapper">
              <input
                type="text"
                placeholder="Type here to start a conversation..."
                className="message-input"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              />
              <div className="send-wrapper">
                <span className="online-status">Online</span>
                <button 
                  className="send-button"
                  onClick={handleSendMessage}
                >
                  <Send className="send-icon" />
                </button>
              </div>
            </div>
            
            <div className="attachment-buttons">
              <button className="attach-button">
                <Paperclip className="attach-icon" />
                Add Attachment
              </button>
              <button className="image-button">
                <Image className="image-icon" />
                Add Image
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;