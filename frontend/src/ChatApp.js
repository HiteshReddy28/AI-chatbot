import ChatBot from "./Chatbot";
import "./Chatapp.css"
function ChatApp(){
    return (
        <>
        <div className="chatapp-container">
            <div className="chatapp-left">
                <h1>Hello</h1>
            </div>
            <div className="chatapp-right">
                <h1>Hello</h1>
                <ChatBot/>
            </div>
        </div>
        
        </>
    );
}

export default ChatApp;
