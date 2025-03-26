from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
from fastapi.middleware.cors import CORSMiddleware

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

@app.post("/generate")
async def generate():
    user_input = "Hi i am unable to pay the loan due to financial difficulties"
    prompt = """<rules>You are an human negotiator,customers come to you to make a finace plan,
    they might not be able to pay there loan due to some reason based on there reason and generate few plan to make them pay the loan</rules>
    <customerdetails>name:Praneth,loanamount:1500,interest_rate:5%,tenue:2years</customerdetails>
    <target>To convence the customer to accept the plan that you present</target>
    <customer_input>"""+user_input+""""</customer_input>"""
    try:
        result = subprocess.run(
            ['ollama', 'run', 'llama3.2', prompt], 
            capture_output=True,
            text=True
        )
        return {"response": result.stdout}
    except Exception as e:
        return {"error": str(e)}

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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
