import os
from dotenv import load_dotenv
from google import genai
from google.genai import errors
from .prompt import CONTEXT, Articles
import time

load_dotenv()

API_KEY = os.environ["GEMINI_API_KEY"]
CLIENT = genai.Client(api_key=API_KEY)

def post(payload, context=CONTEXT, max_attempts=3, client=None) -> Articles:
  '''
  Makes post request to LLM API
  
  :param payload: HN articles for summarising
  :param context: Context prompt explaining LLM role and response type
  :param max_attempts: Number of times to try API call before giving up
  '''
  
  # use default google model if no argument provided
  client = client or CLIENT

  print("Making post request to llm api..")
  for attempt in range(max_attempts):
    try:
      response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=f'{context}\n{payload}',
        config={
          "response_mime_type": "application/json",
          "response_json_schema": Articles.model_json_schema()
        }
      )
      
      summaries = Articles.model_validate_json(response.text)
      print("Done.")
      return summaries
    
    except errors.APIError as e:
      print(f"API error {e} retrying..")
    except Exception as e:
      print(f"Unexpected error {e}, retrying.. ")
      
    if attempt < max_attempts - 1:
      time.sleep(3 ** attempt) #exponential backoff
      
  raise RuntimeError("Could not resolve error, aborting")