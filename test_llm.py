import pytest
from llm import post
from io_helper import read, write

def test_post():
  # load scraped text payload from file
  MOCK_PAYLOAD = read("./test/scraped.txt")
  
  # make post request
  llm_response = post(payload=MOCK_PAYLOAD)
  
  # write response to file for debugging
  write("./test/llm_response_.txt", llm_response.model_dump())
  
  assert llm_response is not None
  
  assert MOCK_PAYLOAD[0]["title"] in llm_response['articles'][0]['title']
  assert MOCK_PAYLOAD[0]["url"] in llm_response['articles'][0]['url']
  assert MOCK_PAYLOAD[1]["title"] in llm_response['articles'][1]['title']
  assert MOCK_PAYLOAD[1]["url"] in llm_response['articles'][1]['url']

# def test_retry():
#   context = ""
#   payload = ""
#   attempts = 3
#   mock_response = 'not json'
  
#   with pytest.raises(RuntimeError, match="Malformed json"):
#     response = post(payload, context, attempts, mock_response)