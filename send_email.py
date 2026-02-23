from email.message import EmailMessage
import os
import smtplib
from dotenv import load_dotenv

# load concealed environmental variables
load_dotenv()

def send(subject, html_content):
  '''Sends an email using Gmail server'''
  
  email = os.environ['EMAIL_ADD']
  
  # build email message
  msg = EmailMessage()
  msg["Subject"] = subject
  msg["From"] = email
  msg["To"] = email
  
  # default to error message if client does not support html
  msg.set_content("Your email client does not support HTML.")
  msg.add_alternative(html_content, subtype="html")
  
  # login to smtp server and send message
  try:
    print("Sending email..")
    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
      smtp.starttls()
      smtp.login(email, os.environ['GOOGLE_APP_PASS'])
      smtp.send_message(msg)
      print("Done.")
  except smtplib.SMTPException as e:
    print(f"Error sending email: {e}")
