from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.openai_helper import get_response_from_openai

app = FastAPI()

# Allow frontend (Streamlit) to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(req: QueryRequest):
    user_query = req.message
    response = get_response_from_openai(user_query)
    return {"response": response}
