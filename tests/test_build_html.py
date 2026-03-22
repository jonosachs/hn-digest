import pytest
from hn_digest.build_html import build
from hn_digest.io_helper import read, write
from hn_digest.prompt import Articles, Entry, Term

def test_build():
  # load in llm text from file
  llm_response_text = read("./tests/read/llm_response.txt")
  mock_response = Articles(**llm_response_text).model_dump()
  
  # build html
  html_content = build(mock_response)

  #write output to file for debugging
  write("./tests/write/html_content_.html", html_content)

  assert mock_response["articles"][0]["title"] in html_content
  assert mock_response["articles"][0]["url"] in html_content
  assert mock_response["articles"][1]["title"] in html_content
  assert mock_response["articles"][1]["url"] in html_content
    