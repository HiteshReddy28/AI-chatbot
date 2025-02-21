import ChatBot from "./Chatbot";
import ChatInterface from "./chatinterface";

function ChatApp(){
    return (
        <>
        <div className="chatapp-container">
            <div className="chatapp-left">

            </div>
            <div className="chatapp-right">
                <ChatInterface/>
            </div>
        </div>
        
        </>
    );
}

export default ChatApp;
