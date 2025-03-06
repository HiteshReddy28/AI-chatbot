import React, { useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function ChatBot() {
    const navigate = useNavigate();

    const verifyUser = async () => {
        const client_id = prompt("Enter your Client ID:");
        const passcode = prompt("Enter your Passcode:");

        try {
            const response = await axios.post("http://localhost:8000/api/verify", { client_id, passcode });

            if (response.data.message === "Access Granted") {
                alert("Access granted! You may now use the chatbot.");
            } else {
                alert("Invalid credentials.");
                navigate("/login");
            }
        } catch (error) {
            alert("Verification failed.");
            navigate("/login");
        }
    };

    useEffect(() => {
        verifyUser();
    }, []);

    return (
        <>  
            <h1>Chatbot Interface</h1>
            <p>You are now inside the chatbot.</p>
        </>
    );
}

export default ChatBot;


// import React, { useState, useEffect } from 'react';
// import { Settings, RefreshCw, ArrowLeft, Send, Paperclip, Image } from 'lucide-react';
// import { useNavigate } from 'react-router-dom';

// const ChatInterface = () => {
//   const [inputMessage, setInputMessage] = useState('');
//   const [messages, setMessages] = useState([]);
//   const [showPrompts, setShowPrompts] = useState(true);
//   const [commonPrompts, setCommonPrompts] = useState([]);

//   const navigate = useNavigate();


//   function onBackClick() {
//     navigate('/');
//   }

//   function handleClick() {
//     navigate('/Signup');
//   }

//   function loginClick() {
//     navigate('/Login');
//   }

//   useEffect(() => {
//     const fetchPrompts = async () => {
//       try {
//         const response = await fetch('http://localhost:8000/prompts');  
//         const data = await response.json();
//         setCommonPrompts(data.prompts);  
//       } catch (error) {
//         console.error('Error fetching prompts:', error);
//       }
//     };

//     fetchPrompts();
//   }, []);

//   const handleSendMessage = async () => {
//     if (inputMessage.trim()) {
//       const userMessage = {
//         text: inputMessage,
//         sender: 'user',
//         timestamp: new Date().toLocaleTimeString(),
//       };

//       setMessages((prev) => [...prev, userMessage]);

//       try {
//         const response = await fetch('http://localhost:8000/chat', {
//           method: 'POST',
//           headers: {
//             'Content-Type': 'application/json',
//           },
//           body: JSON.stringify({ text: inputMessage }),
//         });

//         const data = await response.json();

//         const botMessage = {
//           text: data.response,
//           sender: 'bot',
//           timestamp: new Date().toLocaleTimeString(),
//         };

//         setMessages((prev) => [...prev, botMessage]);
//       } catch (error) {
//         console.error('Error sending message:', error);
//       }

//       setInputMessage('');
//     }
//   };

//   return (
//     <div className="min-h-screen bg-white">

//       <div className="fixed left-0 top-0 w-64 h-screen border-r bg-white">
//         <div className="p-4 flex flex-col h-full">
    
//           <div className="flex items-center mb-6">
//             <ArrowLeft
//               className="w-5 h-5 mr-2 cursor-pointer hover:text-blue-600 transition-colors"
//               onClick={onBackClick}
//             />
//             <h1 className="text-xl font-bold text-blue-900">AI Negotiator</h1>
//           </div>

//           <div className="space-y-3 mb-4">
//             <button className="w-full bg-blue-600 text-white rounded-full py-2 px-4 hover:bg-blue-700 transition-colors" onClick={loginClick}>
//               Login
//             </button>
//             <button className="w-full border border-gray-300 rounded-full py-2 px-4 hover:border-blue-600 hover:text-blue-600 transition-colors" onClick={handleClick}>
//               Sign Up
//             </button>
//             <p className="text-sm text-gray-600">Sign-in to save your conversation</p>
//           </div>


//           <div className="flex items-center text-gray-500 mb-4 cursor-pointer hover:text-blue-600 transition-colors">
//             <RefreshCw className="w-4 h-4 mr-2" />
//             <span>Previous History</span>
//           </div>


//           <div className="mt-auto cursor-pointer hover:text-blue-600 transition-colors">
//             <div className="flex items-center text-gray-500">
//               <Settings className="w-4 h-4 mr-2" />
//               <span>Settings</span>
//             </div>
//           </div>
//         </div>
//       </div>


//       <div className="ml-64 p-8">
//         <div className="max-w-3xl mx-auto">
//           {showPrompts ? (
//             <>

//               <div className="mb-8">
//                 <h2 className="text-4xl font-bold mb-2">Hi there,</h2>
//                 <h3 className="text-4xl font-bold mb-4">What would you like to know?</h3>
//                 <p className="text-gray-500">
//                   Start with one of the most common prompts below or use your own to begin.
//                 </p>
//               </div>

   
//               <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
//                 {commonPrompts.map((prompt, index) => (
//                   <button
//                     key={index}
//                     className="p-4 text-center border bg-white rounded-2xl text-gray-800 hover:border-blue-500 hover:shadow-md transition-all"
//                     onClick={() => setInputMessage(prompt)}
//                   >
//                     {prompt}
//                   </button>
//                 ))}
//               </div>

//               <div className="flex items-center text-gray-500 mb-8 cursor-pointer hover:text-blue-600 transition-colors">
//                 <RefreshCw className="w-4 h-4 mr-2" />
//                 <span>Refresh Prompts</span>
//               </div>
//             </>
//           ) : (

//             <div className="mb-4 space-y-4 max-h-[calc(100vh-200px)] overflow-y-auto">
//               {messages.map((message, index) => (
//                 <div
//                   key={index}
//                   className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
//                 >
//                   <div
//                     className={`max-w-[70%] p-3 rounded-lg ${
//                       message.sender === 'user'
//                         ? 'bg-blue-600 text-white'
//                         : 'bg-gray-100 text-gray-800'
//                     }`}
//                   >
//                     <p>{message.text}</p>
//                     <span className="text-xs opacity-70 mt-1 block">
//                       {message.timestamp}
//                     </span>
//                   </div>
//                 </div>
//               ))}
//             </div>
//           )}

 
//           <div className="bg-gray-50 rounded-lg p-4 shadow-sm">
//             <div className="flex items-center gap-4 mb-4">
//               <input
//                 type="text"
//                 placeholder="Type here to start a conversation..."
//                 className="flex-1 bg-white rounded-lg p-3 outline-none border border-gray-200 focus:border-blue-500 transition-colors"
//                 value={inputMessage}
//                 onChange={(e) => setInputMessage(e.target.value)}
//                 onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
//               />
//               <div className="flex items-center gap-3">
//                 <span className="text-blue-600 font-medium">Online</span>
//                 <button
//                   className="bg-blue-600 text-white p-2 rounded-full hover:bg-blue-700 transition-colors"
//                   onClick={handleSendMessage}
//                 >
//                   <Send className="w-5 h-5" />
//                 </button>
//               </div>
//             </div>

//             <div className="flex gap-2">
//               <button className="flex items-center gap-2 bg-white text-blue-600 rounded-full py-2 px-4 hover:bg-blue-50 transition-colors">
//                 <Paperclip className="w-4 h-4" />
//                 Add Attachment
//               </button>
//               <button className="flex items-center gap-2 bg-white text-blue-600 rounded-full py-2 px-4 hover:bg-blue-50 transition-colors">
//                 <Image className="w-4 h-4" />
//                 Add Image
//               </button>
//             </div>
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// };

// export default ChatInterface;
