import ChatBot from "./Chatbot";

function ChatApp(){
    return (
        <>
        <div className="chatapp-container">
            <div className="chatapp-left">

            </div>
            <div className="chatapp-right">
                <ChatBot/>
            </div>
        </div>
        
        </>
    );
}

export default ChatApp;
