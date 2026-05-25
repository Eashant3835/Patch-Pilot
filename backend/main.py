from fastapi import FastAPI
from app.schemas import AgentRequest
from app.intent import get_intent
from app.planner import get_plan

app = FastAPI()

@app.get("/")
async def root():
    pass

@app.post("/run-agent")
async def run_agent(request: AgentRequest):
    result = await get_intent(request.task)
    if "task" in result["intents"]:
        task = await get_plan(request.task)
        return {"task": task}
    elif "chat" in result["intents"]:
        return {"message": "Hi! What can I help you with today?"}
    else:
        return {"intent": result}