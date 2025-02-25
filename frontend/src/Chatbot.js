import React, { useState, useEffect, useRef } from "react";
import axios from "axios";

const ChatBot = () => { 
  console.log("Chatbot Component Loaded");  

  const [messages, setMessages] = useState([]); // Stores all messages
  const [input, setInput] = useState(""); // Tracks the user's input
  const [loading, setLoading] = useState(false); // Indicates when the LLM is responding
  const chatEndRef = useRef(null); 

  // FastAPI Backend URL
  const API_URL = "http://localhost:8000/chat";  

  // Send Message to FastAPI Backend
  const sendMessageToLLM = async (userMessage) => {
    setLoading(true);
    try {
      const response = await axios.post(API_URL, { message: userMessage });

      // Append LLM Response to Chat
      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: "bot", text: response.data.response },
      ]);
    } catch (error) {
      console.error("Error communicating with LLaMA backend:", error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: "bot", text: "Error: Unable to get a response from LLaMA" },
      ]);
    }
    setLoading(false);
  };

  // Handle Sending Message
  const handleSendMessage = () => {
    if (input.trim() === "") return;
    
    setMessages([...messages, { sender: "user", text: input }]); // Show user message
    sendMessageToLLM(input); // Call the backend
    setInput(""); // Clear the input field
  };

  // Scroll to the latest message
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  return (
    <div className="flex flex-col h-screen bg-gray-100 p-6">
      {/* Chat Window */}
      <div className="flex-grow overflow-y-auto mb-4">
        <div className="space-y-4">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${
                message.sender === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`${
                  message.sender === "user"
                    ? "bg-blue-500 text-white"
                    : "bg-gray-300 text-black"
                } p-3 rounded-lg max-w-xs break-words`}
              >
                {message.text}
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex justify-start">
              <div className="bg-gray-300 text-black p-3 rounded-lg max-w-xs break-words">
                Typing...
              </div>
            </div>
          )}
          <div ref={chatEndRef} />
        </div>
      </div>

      {/* Input Field */}
      <div className="flex">
        <input
          type="text"
          className="flex-grow p-2 border rounded-l-lg border-gray-300 focus:outline-none"
          placeholder="Type a message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
        />
        <button
          className="bg-blue-500 text-white px-4 py-2 rounded-r-lg hover:bg-blue-600"
          onClick={handleSendMessage}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatBot;

