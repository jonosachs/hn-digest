import pytest
from io_helper import read
from send_email import send

def test_send():
  # load in html content
  content = read("./test/read/html_content.html")

  # send test email
  send("test", content)