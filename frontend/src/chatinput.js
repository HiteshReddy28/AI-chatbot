// ChatInput.js
import React, { useState } from 'react';
import { Plus, Image, Send } from 'lucide-react';

const ChatInput = ({ onSendMessage }) => {
  const [message, setMessage] = useState('');

  const handleSend = () => {
    if (message.trim()) {
      onSendMessage(message);
      setMessage('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-gray-100 rounded-xl p-4">
        <div className="flex items-center space-x-4">
          <input
            type="text"
            placeholder="Type here to start a conversation..."
            className="flex-1 bg-transparent outline-none text-gray-700"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleKeyPress}
          />
          
          <div className="flex items-center space-x-4">
            <button className="flex items-center text-gray-400 hover:text-gray-600">
              <Plus className="w-5 h-5 mr-2" />
              <span className="text-sm">Add Attachment</span>
            </button>
            
            <button className="flex items-center text-gray-400 hover:text-gray-600">
              <Image className="w-5 h-5 mr-2" />
              <span className="text-sm">Use Image</span>
            </button>
            
            <div className="w-px h-6 bg-gray-300" />
            
            <span className="text-blue-600 text-sm">Online</span>
            
            <button 
              onClick={handleSend}
              className="bg-blue-900 text-white p-2 rounded-full hover:bg-blue-800 transition-colors"
              aria-label="Send message"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatInput;