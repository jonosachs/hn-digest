import pytest
from build_html import build
from mock_payload import MOCK_PAYLOAD
from pathlib import Path


def test_build():
  html_content = build(MOCK_PAYLOAD)
  
  assert MOCK_PAYLOAD[0]["title"] in html_content
  assert MOCK_PAYLOAD[0]["url"] in html_content
  assert MOCK_PAYLOAD[1]["title"] in html_content
  assert MOCK_PAYLOAD[1]["url"] in html_content
  
  
  
  
  