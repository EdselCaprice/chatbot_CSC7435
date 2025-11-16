import { useState, useRef, useEffect } from 'react';
const ENDPOINT = process.env.REACT_APP_API_URL || "http://localhost:5000";
function App() {
    const [userMessage, setUserMessage] = useState(""); //track user input
    const [messages, setMessages] = useState([]); //tracks all messages to be displayed in the UI
    const chatboxRef = useRef(null); //use for auto scrolling scrollbar. See first useEffect hook below
    const [chatbotHistory, setChatbotHistory] = useState([]); //use for storing chat history to be provided to the LLM on the backend 
    
    //add message to messages state with timestamp
    const addMessage = (message, role) => {
        const now = new Date();
        const timestamp = now.toLocaleTimeString('en-US', {
          hourFormat: '24',
        });
        const newMessage = { content: message, role, timestamp: timestamp };
        setMessages((prevMessages) => [...prevMessages, newMessage]);
    };

    //auto scroll chatbox to bottom when messages state changes
    useEffect(() => {
        if (chatboxRef.current) {
          chatboxRef.current.scrollTop = chatboxRef.current.scrollHeight;
        }
      }, [messages])

    //fetch welcome message from backend on initial page load
    useEffect(() => {
        fetch(ENDPOINT + "/hello", {
            method: "GET",
            cache: "no-cache",
            headers: {"content-type":"application/json"},
        })
            .then((response) => response.json())
            .then((responseData) => {addMessage(responseData, 'bot')
            });
        }, []);

    //form submission handler
    function onSubmit(e) {
        e.preventDefault();
        addMessage(userMessage, 'user');
        fetch(ENDPOINT + "/chatbot", {
            method: "POST",
            cache: "no-cache",
            headers: {"content-type":"application/json"},
            body: JSON.stringify({question: userMessage, chat_history: chatbotHistory})
          })
            .then((response) => response.json())
            .then((responseData) => (addMessage(responseData[0], 'bot'),
                setChatbotHistory(responseData[1])
                ));
        setUserMessage("")
    }   
    
    //display user message
    const UserResponse = (props) => {
        
        return (
            <div class="d-flex align-items-start justify-content-end mb-3">
              <div class="pe-2 me-1" style={{maxWidth: "348px"}}>
                <div class="text-light p-3 mb-1 rounded-3" style={{background: "#1982FC"}}>{props.message}</div>
                    <div class="fw-bold text-muted">You</div>
                    <div class="ms-2">
                        {props.timestamp}
                    </div>
              </div>
            </div>
        )
    }
    
    //display system/bot message
    const SystemResponse = (props) => {
        return (
            <>
            <div class="d-flex align-items-start justify-content-start mb-3">
              <div class="ps-2 ms-1" style={{maxWidth: "548px"}}>
                <div class="text-light p-3 mb-1 rounded-3" style={{background: "rgba(255, 255, 255, .04)"}} >
                <div className='text-light' dangerouslySetInnerHTML={{ __html: props.message }} />
                </div>
                <div class="fw-bold text-muted">TaxResearch.AI</div>
                <div class="ms-2">
                    {props.timestamp}
                </div>
              </div>
            </div>
    
            </>
        )
    }
    const style = {
        width: "100%",
        "@media (min-width: 768px)": {
          width: "50%",
        },
      };

  return (
    <div className="container" style={style} >
    <form onSubmit={onSubmit} className='mt-1'>
    <div className="col-lg-12">
        <div className="card h-100 border bg-dark rounded-3">
            <div className="card-header d-flex align-items-center justify-content-between w-100 p-sm-4 p-3">
                <div className="d-flex align-items-center pe-3">
                    <h6 class="mb-0 px-1 mx-2 text-white">TaxResearch.AI</h6>
                    <div className="bg-success rounded-circle" style={{width: "8px", height: "8px"}}></div>
                </div>
            </div>

            <div className="card-body swiper scrollbar-hover overflow-hidden w-100 pb-0 border-light border-1">
                <div className="swiper-wrapper">
                    <div className="chat-box scrollable w-100 overflow-auto auto" style={{height: 600}} ref={chatboxRef}>
                        {messages.map((message, i) => (
                            message.role === 'user' ? (
                                <UserResponse message={message.content} timestamp={message.timestamp} key={i} />
                            ) : (
                                <SystemResponse message={message.content} timestamp={message.timestamp} key={i} />
                            )
                        ))}
                    </div>
                </div>
            </div>

            <div className="card-footer d-sm-flex w-100 border-0 pt-3 pb-3 px-4">
                <div className="position-relative w-100 me-2 mb-3 mb-sm-0">
                    <input
                        type="text"
                        className="form-control form-control-lg"
                        style={{ paddingRight: "85px" }}
                        onChange={(e) => setUserMessage(e.target.value)}
                        value={userMessage}
                        placeholder="Type your message"
                    />
                </div>
                <button type="submit" className="btn btn-primary btn-icon btn-lg d-none d-sm-inline-flex ms-1">
                    <i className="bx bx-send"></i>
                </button>
                <button type="submit" className="btn btn-primary btn-lg w-100 d-sm-none">
                    <i className="bx bx-send fs-xl me-2"></i>
                    Send
                </button>
            </div>
        </div>
    </div>
</form>
Created by <a href="https://www.linkedin.com/in/edselcaprice/">Edsel Caprice</a> <a href="https://www.linkedin.com/in/edselcaprice/"><i class='bx bxl-linkedin-square'></i></a>
<br />




</div>
  );
}

export default App;
