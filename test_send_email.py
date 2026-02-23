import pytest
from io_helper import read
from send_email import send

def test_send():
  # load in html content
  content = read("./test/html_content_.html")

  # send test email
  send("test", content)