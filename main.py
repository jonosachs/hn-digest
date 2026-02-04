from hn_scraper import scrape
from llm import post
from send_email import send
from build_html import build
from io_helper import write

def run():
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
