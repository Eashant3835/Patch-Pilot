from dotenv import load_dotenv
from groq import AsyncGroq
import json

load_dotenv()
client = AsyncGroq()

SYSTEM_PROMPT = (
    "You are an AI component in a chrome web extension, whose job is to generate a backup plan when given a failed step and a page snapshot. "
    'Return the plan as JSON in this exact format: {"plan": [{"action": "click", "target": "element", "value": "optional"}]}. '
    "Only include value if the action requires it."
)

async def get_planB(failed_step,page_snapshot,task):
    USER_PROMPT = f"You are assisting in creating a Plan B for the following task: {task}.The failed step was {failed_step} and the current page snapshot where the page failed is {page_snapshot}"
    response = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
    messages=[
      {
        "role": "system",
        "content": SYSTEM_PROMPT
      },
      {
        "role": "user",
        "content": USER_PROMPT
      }
    ]
    )
    parsed_response = json.loads(response.choices[0].message.content)
    return parsed_response