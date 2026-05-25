from dotenv import load_dotenv
from groq import AsyncGroq
import json

load_dotenv()
client = AsyncGroq()

SYSTEM_PROMPT = (
    "You are an AI whose only job is to classify a message into one or more of the following categories. "
    "A message can belong to more than one category. "
    "-> Task: When a user assigns a task for the browser to do. Eg: Open LinkedIn and find jobs. "
    "-> Chat: When the user is just greeting or making small talk. Eg: How are you doing. "
    "-> Memory: When the user wants something remembered. Eg: My usual workflow is... "
    "-> Other: If it does not fit any category. "
    'Respond ONLY with JSON in this exact format: {"intents": ["task", "memory"]} - no extra text.'
)

async def get_intent(user_prompt):
    response = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
    messages=[
      {
        "role": "system",
        "content": SYSTEM_PROMPT
      },
      {
        "role": "user",
        "content": user_prompt
      }
    ]
    )
    parsed_response = json.loads(response.choices[0].message.content)
    return parsed_response


