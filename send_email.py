from email.message import EmailMessage
import os
import smtplib
from dotenv import load_dotenv

load_dotenv()

def send(subject, html_content):
  email = os.environ['EMAIL_ADD']
  
  msg = EmailMessage()
  msg["Subject"] = subject
  msg["From"] = email
  msg["To"] = email
  
  msg.set_content("Your email client does not support HTML.")
  msg.add_alternative(html_content, subtype="html")
  
  with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
    smtp.starttls()
    smtp.login(email, os.environ['GOOGLE_APP_PASS'])
    smtp.send_message(msg)
    print("Email sent.")
    
