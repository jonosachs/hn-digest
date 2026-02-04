from hn_scraper import scrape
from llm import post
from send_email import send
from build_html import build
from io_helper import write
import os

def run():
  print("Checking credentials")
  if not all([os.environ.get("GEMINI_API_KEY"),
              os.environ.get('EMAIL_ADD'),
              os.environ.get('GOOGLE_APP_PASS')]):
    raise RuntimeError("Could not load credentials")
  
  #get top <limit> latest articles from HN
  print("Scraping HN...")
  articles = scrape(limit=5)
  print(f"Scraped {len(articles)} articles.")
  
  #send articles to llm for response
  print("Sending payload to LLM API...")
  llm_response = post(payload=articles)
  print(f"LLM response recieved ({type(llm_response)}).")
  
  #write raw llm response to file for debugging
  write("raw.txt", llm_response)
        
  #build html content from response
  print("Building HTML..")
  html_content = build(llm_response)
  
  #email formatted content
  send("HN Digest", html_content)
  print("Done.")

if __name__ == "__main__":
  run()
