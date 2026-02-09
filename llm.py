import os
from dotenv import load_dotenv
from google import genai
from google.genai import errors
from prompt import CONTEXT
import json

load_dotenv()
API_KEY = os.environ["GEMINI_API_KEY"]
CLIENT = genai.Client(api_key=API_KEY)

def post(payload, attempts=3) -> list[dict]:
  try:
    response = CLIENT.models.generate_content(
        model="gemini-3-flash-preview",
        contents=f'{CONTEXT}\n{payload}',
        config={"response_mime_type": "application/json"}
    )
  except Exception as e:
    raise RuntimeError(f"LLM API error: {e}")
  
  try:
    json_response = json.loads(response.text)
  except json.JSONDecodeError as e:
    print(f"Malformed json, retrying LLM call.. {e}")
    if attempts > 0: 
      return post(payload, attempts - 1)
    else: 
      raise RuntimeError(f"Malformed json: {e}")
    
  return json_response