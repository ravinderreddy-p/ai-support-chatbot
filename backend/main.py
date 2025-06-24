from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.openai_helper import get_response_from_openai, log_feedback

app = FastAPI()

# Allow frontend (Streamlit) to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request body model for feedback
class FeedbackRequest(BaseModel):
    feedback: str
    user_query: str
    response: str

class QueryRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(req: QueryRequest):
    user_query = req.message
    response = get_response_from_openai(user_query)
    return {"response": response}

@app.post("/feedback")
async def receive_feedback(feedback_data: FeedbackRequest):
    feedback = feedback_data.feedback
    user_query = feedback_data.user_query
    bot_reply = feedback_data.response
    
    # Log the feedback to a file
    log_feedback(feedback, user_query, bot_reply)
    
    return {"status": "success", "message": "Feedback logged successfully"}
