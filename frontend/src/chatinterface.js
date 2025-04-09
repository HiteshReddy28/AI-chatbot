import React, { useState, useEffect, useRef } from 'react';
import { Settings, RefreshCw, ArrowLeft, Send, Paperclip, Image, Trash2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import './Chatapp.css';
import Navbar from "./navbar.js";

const ChatInterface = () => {
  const [inputMessage, setInputMessage] = useState('');
  const [messages, setMessages] = useState([]);
  const [isBotTyping, setIsBotTyping] = useState(false);
  const messagesEndRef = useRef(null);
  const navigate = useNavigate();

  const commonPrompts = [
    'Can I refinance my existing loan?',
    'Does applying for a loan impact my credit score?',
    'How is my financial risk assessed for a loan?',
    'What are Debt-to-Income (DTI)?'
  ];

  useEffect(() => {
    const token = localStorage.getItem("token");
    const client_id = localStorage.getItem("client_id");

    if (!token || !client_id) {
      alert("You must be logged in to access the chatbot.");
      navigate("/login");
    } else {
      fetchChatHistory(client_id, token);
    }
  }, [navigate]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const clearChatHistory = async () => {
    const client_id = localStorage.getItem("client_id");
    const token = localStorage.getItem("token");

    if (!client_id || !token) {
      console.error("User is not authenticated.");
      return;
    }

    try {
      await fetch(`http://localhost:8000/api/chat/clear/${client_id}`, {
        method: "DELETE",
        headers: { "Authorization": `Bearer ${token}` },
      });
      setMessages([]);
      alert("Chat history cleared successfully.");
    } catch (error) {
      console.error("Error clearing chat history:", error);
    }
  };

  const storeChatMessage = async (sender, message) => {
    const client_id = localStorage.getItem("client_id");
    const token = localStorage.getItem("token");

    if (!client_id || !token) {
      console.error("User is not authenticated.");
      return;
    }

    try {
      await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify({ client_id, sender, message }),
      });
    } catch (error) {
      console.error("Error storing chat message:", error);
    }
  };

  const fetchChatHistory = async (client_id, token) => {
    try {
      const response = await fetch(`http://localhost:8000/api/chat/${client_id}`, {
        method: "GET",
        headers: { "Authorization": `Bearer ${token}` },
      });

      const data = await response.json();
      if (data.chat_history) {
        setMessages(data.chat_history.map((msg) => ({
          text: msg.message,
          sender: msg.sender,
          timestamp: new Date(msg.timestamp).toLocaleTimeString(),
        })));
      }
    } catch (error) {
      console.error("Error fetching chat history:", error);
    }
  };

  const handleSendMessage = async () => {
    if (inputMessage.trim()) {
      const userMessage = {
        text: inputMessage,
        sender: "user",
        timestamp: new Date().toLocaleTimeString(),
      };

      setMessages((prev) => [...prev, userMessage]);
      storeChatMessage("user", inputMessage);
      setInputMessage('');
      setIsBotTyping(true);

      const response = await callLlamaAPI(inputMessage);

      setIsBotTyping(false);

      if (response && response.negotiation_response) {
        const botMessage = {
          text: response.negotiation_response,
          sender: "bot",
          timestamp: new Date().toLocaleTimeString(),
        };

        setMessages((prev) => [...prev, botMessage]);
        storeChatMessage("bot", response.negotiation_response);
      } else {
        const errorMessage = {
          text: "Sorry, I encountered an error. Please try again.",
          sender: "bot",
          timestamp: new Date().toLocaleTimeString(),
        };
        setMessages((prev) => [...prev, errorMessage]);
      }
    }
  };

  const callLlamaAPI = async (prompt) => {
    try {
      const response = await fetch('http://localhost:8000/api/negotiate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          "Authorization": `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify({
          client_id: localStorage.getItem("client_id"),
          requested_changes: prompt,
          prompt: prompt
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error("Error calling Llama API:", error);
      return null;
    }
  };

  return (
    <>
      <Navbar />
      <div className="chat-container">
        <div className="sidebar">
          <div className="sidebar-content">
            <div className="sidebar-header">
              <ArrowLeft className="back-button" onClick={() => navigate('/')} />
              <h1 className="app-title">AI Negotiator.</h1>
            </div>
            <div className="history-button">
              <RefreshCw className="history-icon" />
              <span>Previous History</span>
            </div>
            <div className="settings-button">
              <Settings className="settings-icon" />
              <span>Settings</span>
            </div>
            <button className="clear-chat-button" onClick={clearChatHistory}>
              <Trash2 className="clear-icon" /> Clear Chat
            </button>     
          </div>
        </div>
        
        <div className="main-content">
          <div className="chat-wrapper">
            <div className="prompt-header">
              <h2>Hi there,</h2>
              <h3>What would you like to know?</h3>
              <p className="prompt-subtext">Start with one of the most common prompts below or use your own to begin</p>
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

            <div className="message-container">
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`message-row ${message.sender === 'user' ? 'user' : 'bot'}`}
                >
                  <div className={`message-bubble ${message.sender === 'user' ? 'user-message' : 'bot-message'}`}>
                    <div
                      dangerouslySetInnerHTML={{
                        __html: message.text
                          .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
                          .replace(/•/g, "<li>")
                          .replace(/<li>(.*?)<\/li>/g, "<ul><li>$1</li></ul>")
                          .replace(/\n/g, "<br/>")
                      }}
                    />
                    <span className="message-time">{message.timestamp}</span>
                  </div>
                </div>
              ))}

              {isBotTyping && (
                <div className="message-row bot">
                  <div className="message-bubble bot-message typing-indicator">
                    <span>Replying</span><span className="dot">.</span><span className="dot">.</span><span className="dot">.</span>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

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
                  <button className="send-button" onClick={handleSendMessage}>
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
    </>
  );
};

export default ChatInterface;
