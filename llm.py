import os
from dotenv import load_dotenv
from google import genai
from prompt import base_prompt
import json

load_dotenv()

def post(payload: str) -> str:
  api_key = os.getenv("GEMINI_API_KEY")
  client = genai.Client(api_key=api_key)
  prompt = base_prompt()
  
  try:
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=f'{prompt}\n{payload}'
    )
  except Exception as e:
    raise RuntimeError("Bad server response: {e}")

  return json.loads(response.text)
  