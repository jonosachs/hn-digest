import pytest
from build_html import build
from io_helper import read, write

def test_build():
  # load in llm text from file
  MOCK_RESPONSE = read("./test/llm_response.txt")

  # build html
  html_content = build(MOCK_RESPONSE)

  #write output to file for debugging
  write("./test/email_.html", html_content)

  assert MOCK_RESPONSE["articles"][0]["title"] in html_content
  assert MOCK_RESPONSE["articles"][0]["url"] in html_content
  assert MOCK_RESPONSE["articles"][1]["title"] in html_content
  assert MOCK_RESPONSE["articles"][1]["url"] in html_content
    