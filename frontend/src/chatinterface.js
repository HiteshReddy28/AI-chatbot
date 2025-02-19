import React, { useState } from 'react';
import { Settings, RefreshCw, ArrowLeft, Send, Paperclip, Image } from 'lucide-react';

const ChatInterface = ({ onBackClick }) => {
  const [inputMessage, setInputMessage] = useState('');
  const [messages, setMessages] = useState([]);
  const [showPrompts, setShowPrompts] = useState(true);

  // Predefined bot responses
  const botResponses = {
    'Can I refinance my existing loan?': 
      "Yes, you can refinance your existing loan. The process involves applying for a new loan to pay off your current one, potentially getting better terms or interest rates. We'll need to review your current loan terms and credit status to determine eligibility.",
    
    'Does applying for a loan impact my credit score?':
      "Yes, applying for a loan typically results in a hard inquiry on your credit report, which can temporarily lower your score by a few points. However, this impact is usually minimal and your score can recover within a few months of responsible credit use.",
    
    'How is my financial risk assessed for a loan?':
      "Financial risk assessment involves evaluating several factors including your credit score, income, employment history, debt-to-income ratio, and payment history. We also consider your assets and any collateral you're offering.",
    
    'What are Debt-to-Income (DTI)?':
      "Debt-to-Income (DTI) ratio is a financial measure that compares your monthly debt payments to your monthly gross income. It's calculated by dividing your total monthly debt payments by your monthly gross income. A lower DTI ratio is generally better for loan approval.",
  };

  // Default response for undefined queries
  const defaultResponse = "I understand your question. Let me help you with that. Could you please provide more specific details about your inquiry?";

  const commonPrompts = [
    'Can I refinance my existing loan?',
    'Does applying for a loan impact my credit score?',
    'How is my financial risk assessed for a loan?',
    'What are Debt-to-Income (DTI)?'
  ];

  const handleSendMessage = () => {
    if (inputMessage.trim()) {
      // Add user message
      const userMessage = {
        text: inputMessage,
        sender: 'user',
        timestamp: new Date().toLocaleTimeString(),
      };

      // Get bot response
      const botMessage = {
        text: botResponses[inputMessage] || defaultResponse,
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString(),
      };

      // Update messages and hide prompts
      setMessages(prev => [...prev, userMessage, botMessage]);
      setInputMessage('');
      setShowPrompts(false);
    }
  };

  return (
    <div className="min-h-screen bg-white">
      {/* Sidebar */}
      <div className="fixed left-0 top-0 w-64 h-screen border-r bg-white">
        <div className="p-4 flex flex-col h-full">
          {/* Header */}
          <div className="flex items-center mb-6">
            <ArrowLeft 
              className="w-5 h-5 mr-2 cursor-pointer hover:text-blue-600 transition-colors" 
              onClick={onBackClick} 
            />
            <h1 className="text-xl font-bold text-blue-900">AI Negotiator.</h1>
          </div>

          {/* Auth Buttons */}
          <div className="space-y-3 mb-4">
            <button className="w-full bg-blue-600 text-white rounded-full py-2 px-4 hover:bg-blue-700 transition-colors">
              Login
            </button>
            <button className="w-full border border-gray-300 rounded-full py-2 px-4 hover:border-blue-600 hover:text-blue-600 transition-colors">
              Sign Up
            </button>
            <p className="text-sm text-gray-600">Sign-in to save your conversation</p>
          </div>

          {/* History Section */}
          <div className="flex items-center text-gray-500 mb-4 cursor-pointer hover:text-blue-600 transition-colors">
            <RefreshCw className="w-4 h-4 mr-2" />
            <span>Previous History</span>
          </div>

          {/* Settings (Positioned at bottom) */}
          <div className="mt-auto cursor-pointer hover:text-blue-600 transition-colors">
            <div className="flex items-center text-gray-500">
              <Settings className="w-4 h-4 mr-2" />
              <span>Settings</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="ml-64 p-8">
        <div className="max-w-3xl mx-auto">
          {showPrompts ? (
            <>
              {/* Welcome Section */}
              <div className="mb-8">
                <h2 className="text-4xl font-bold mb-2">Hi there,</h2>
                <h3 className="text-4xl font-bold mb-4">What would you like to know?</h3>
                <p className="text-gray-500">
                  Start with one of most common prompts below or use your own to begin
                </p>
              </div>

              {/* Prompt Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
                {commonPrompts.map((prompt, index) => (
                  <button
                    key={index}
                    className="p-4 text-center border bg-white rounded-2xl text-gray-800 hover:border-blue-500 hover:shadow-md transition-all"
                    onClick={() => setInputMessage(prompt)}
                  >
                    {prompt}
                  </button>
                ))}
              </div>

              {/* Refresh Prompts */}
              <div className="flex items-center text-gray-500 mb-8 cursor-pointer hover:text-blue-600 transition-colors">
                <RefreshCw className="w-4 h-4 mr-2" />
                <span>Refresh Prompts</span>
              </div>
            </>
          ) : (
            /* Chat Messages */
            <div className="mb-4 space-y-4 max-h-[calc(100vh-200px)] overflow-y-auto">
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[70%] p-3 rounded-lg ${
                      message.sender === 'user'
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-100 text-gray-800'
                    }`}
                  >
                    <p>{message.text}</p>
                    <span className="text-xs opacity-70 mt-1 block">
                      {message.timestamp}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Chat Input Section */}
          <div className="bg-gray-50 rounded-lg p-4 shadow-sm">
            <div className="flex items-center gap-4 mb-4">
              <input
                type="text"
                placeholder="Type here to start a conversation..."
                className="flex-1 bg-white rounded-lg p-3 outline-none border border-gray-200 focus:border-blue-500 transition-colors"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              />
              <div className="flex items-center gap-3">
                <span className="text-blue-600 font-medium">Online</span>
                <button 
                  className="bg-blue-600 text-white p-2 rounded-full hover:bg-blue-700 transition-colors"
                  onClick={handleSendMessage}
                >
                  <Send className="w-5 h-5" />
                </button>
              </div>
            </div>
            
            <div className="flex gap-2">
              <button className="flex items-center gap-2 bg-white text-blue-600 rounded-full py-2 px-4 hover:bg-blue-50 transition-colors">
                <Paperclip className="w-4 h-4" />
                Add Attachment
              </button>
              <button className="flex items-center gap-2 bg-white text-blue-600 rounded-full py-2 px-4 hover:bg-blue-50 transition-colors">
                <Image className="w-4 h-4" />
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