from fastapi import FastAPI
from app.schemas import AgentRequest
from app.router import get_intent

app = FastAPI()

@app.get("/")
async def root():
    pass

@app.post("/run-agent")
async def run_agent(request: AgentRequest):
    result = await get_intent(request.task)
    print(result)
    return { "intent": result }