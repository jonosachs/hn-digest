import pytest
from llm import post

def test_post():
  context = ""
  payload = "test"
  attempts = 1
  test_response = None
  response = post(payload, context, attempts, test_response)
  
  print(response) #use pytest -s to show
  
  assert response is not None
  assert len(response) > 0
  assert type(response) == dict 

def test_retry():
  context = ""
  payload = ""
  attempts = 3
  test_response = 'not json'
  
  with pytest.raises(RuntimeError, match="Malformed json"):
    response = post(payload, context, attempts, test_response)
  