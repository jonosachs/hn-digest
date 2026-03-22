import pytest
from hn_digest.io_helper import read
from hn_digest.send_email import send

def test_send():
  # load in html content
  content = read("./tests/read/html_content.html")

  # send test email
  send("test", content)