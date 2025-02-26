from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime
import subprocess


app = FastAPI()


origins = [
    "http://localhost:3000",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)
class PromptRequest(BaseModel):
    prompt: str

@app.post("/api/ollama")
async def ollama_inference(request: PromptRequest):
    try:
        
        result = subprocess.run(
            ['ollama', 'run', 'llama3.2', request.prompt], 
            capture_output=True,
            text=True
        )
        
        return {"response": result.stdout}
    except Exception as e:
        return {"error": str(e)}
    

@app.get("/")
async def read_root():
    return {"message": "Hello from FastAPI"}

COMMON_PROMPTS = [
    "Can I refinance my existing loan?",
    "Does applying for a loan impact my credit score?",
    "How is my financial risk assessed for a loan?",
    "What are Debt-to-Income (DTI)?",
]


class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    timestamp: str




# @app.post("/api/chat", response_model=ChatResponse)
# async def chat_endpoint(request: ChatRequest):
#     try:
#         bot_response = process_message(request.message)
        
#         return {
#             "response": bot_response,
#             "timestamp": datetime.now().strftime("%H:%M:%S")
#         }
        
#     except Exception as e:
#         raise HTTPException(
#             status_code=500, 
#             detail=str(e)
#         )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
