from fastapi import FastAPI
from app.schemas import AgentRequest
from app.intent import get_intent
from app.planner import get_plan
from fastapi import WebSocket
from app.replanner import get_planB

app = FastAPI()

active_sessions = {}

@app.get("/")
async def root():
    pass

@app.post("/run-agent")
async def run_agent(request: AgentRequest):
    result = await get_intent(request.task)
    if "task" in result["intents"]:
        plan = await get_plan(request.task)
        if active_sessions.get(request.session_id):
            active_sessions[request.session_id]["plan"] = plan
        else:
            return {"error":"Extension not connected"}
        active_sessions[request.session_id]["task"] = request.task
        return {"plan": plan}
    elif "chat" in result["intents"]:
        return {"message": "Hi! What can I help you with today?"}
    else:
        return {"intent": result}

    
@app.websocket("/ws")
async def ws(websocket: WebSocket):
    await websocket.accept()
    handshake = await websocket.receive_json()

    session_ID = handshake["session_ID"]
    active_sessions[session_ID] = {"websocket": websocket}
    current_step = 0
    while True:
        recieved = await websocket.receive_json()
        if current_step == len(active_sessions[session_ID]["plan"]):
            await websocket.send_json({"status": "complete","message":"Task Complete"})
            break
        elif recieved["status"] == "successful":
            current_step += 1
            plan = active_sessions[session_ID]["plan"]
            next_step = plan[current_step]
            await websocket.send_json(next_step)
        else:
            task = active_sessions[session_ID]["task"]
            page_snapshot = recieved["snapshot"]
            new_plan = await get_planB(current_step,page_snapshot,task)
            active_sessions[session_ID]["plan"] = new_plan
            current_step = 0
        