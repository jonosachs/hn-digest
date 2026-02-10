import os
from dotenv import load_dotenv
from google import genai
from google.genai import errors
from prompt import CONTEXT
import json
import time

load_dotenv()
API_KEY = os.environ["GEMINI_API_KEY"]
CLIENT = genai.Client(api_key=API_KEY)

def post(payload, context=CONTEXT, attempts=3, test_response=None) -> list[dict]:
  print("Attempting llm api call..")
  attempts -= 1
  
  if not test_response:
    try:
      response = CLIENT.models.generate_content(
        model="gemini-3-flash-preview",
        contents=f'{context}\n{payload}',
        config={"response_mime_type": "application/json"}
      )
      response_text = response.text
    except errors.ClientError as e:
      if e.code == 429:
        if attempts > 0:
          print(f"LLM resource exhausted, retrying.. (attempts remaining: {attempts})")
          time.sleep(2)
          return post(payload, context, attempts, test_response)
      else:
        raise RuntimeError(f"LLM API error [{e.code}]: {e}")
  else:
    response_text = test_response
    
  # parse LLM response as json
  try:
    json_response = json.loads(response_text)
  except json.JSONDecodeError as e:
    if attempts > 0:
      print(f"Malformed json response, retrying LLM call.. (attempts remaining: {attempts})")
      time.sleep(1)
      return post(payload, context, attempts, test_response)
    else: 
      raise RuntimeError(f"Malformed json: {e}")
  
  return json_response