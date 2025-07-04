from fastapi import FastAPI
from pydantic import BaseModel
from heat_news_agent.agent import get_latest_news  # import tool directly

app = FastAPI()

class PromptRequest(BaseModel):
    topic: str

@app.post("/prompt")
def prompt(request: PromptRequest):
    result = get_latest_news(request.topic)
    return result
