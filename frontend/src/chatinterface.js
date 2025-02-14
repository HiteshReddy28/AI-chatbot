import React, { useState } from 'react';
import { Send } from 'lucide-react';

const ChatInterface = () => {
  const [messages, setMessages] = useState([
    { id: 1, text: "Hello! How can I help you today?", sender: "bot" }
  ]);
  const [newMessage, setNewMessage] = useState("");

  const handleSend = () => {
    if (newMessage.trim()) {
      const userMessage = {
        id: messages.length + 1,
        text: newMessage,
        sender: "user"
      };
      
      const botMessage = {
        id: messages.length + 2,
        text: "Thanks for your message! This is a demo response.",
        sender: "bot"
      };
      
      setMessages([...messages, userMessage, botMessage]);
      setNewMessage("");
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-[600px] w-full max-w-2xl mx-auto border rounded-lg shadow-lg" style={{ backgroundColor: '#002768' }}>
      {/* Chat Header */}
      <div className="p-4 border-b rounded-t-lg bg-opacity-90" style={{ backgroundColor: '#001845' }}>
        <h2 className="text-xl font-semibold text-white">Chatbot</h2>
      </div>

      {/* Messages Area */}
      <div className="flex-1 p-4 overflow-y-auto">
        <div className="space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] p-3 rounded-lg ${
                  message.sender === 'user'
                    ? 'bg-white text-gray-800 rounded-br-none'
                    : 'bg-blue-200 text-gray-800 rounded-bl-none'
                }`}
              >
                {message.text}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Input Area */}
      <div className="p-4 border-t" style={{ backgroundColor: '#001845' }}>
        <div className="flex space-x-2">
          <textarea
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
            className="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white text-gray-800"
            rows="1"
          />
          <button
            onClick={handleSend}
            className="p-2 bg-white text-blue-900 rounded-lg hover:bg-blue-50 focus:outline-none focus:ring-2 focus:ring-blue-300"
          >
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;