from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import json
from langchain_core.messages import SystemMessage, HumanMessage

SYSTEM_PROMPT = (
    "You are an AI whose purpose is to generate a step by step plan to accomplish a task in google chrome. "
    'Return the plan as JSON in this exact format: {"plan": [{"action": "click", "target": "element", "value": "optional"}]}. '
    "Only include value if the action requires it. "
    "Do not wrap the response in markdown. Return raw JSON only. "
    "Only use these actions: navigate, click, type, scroll, select."
)

load_dotenv()
client = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.1,
    max_retries=2,
)

async def get_plan(task):
    USER_PROMPT = f"The task you have been assigned is {task}. Generate the step by step plan to accomplish this task in chrome using the system guidelines"
    response = await client.ainvoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=USER_PROMPT)
    ])
    parsed_response = json.loads(response.content)
    return parsed_response