from hn_scraper import scrape
from llm import post
from pathlib import Path
from write_to_file import write

def run():
  #get top # latest articles from HN
  print("Scraping HN...")
  articles = scrape(limit=2)
  print(f"Scraped {len(articles)} articles.")
  
  #pass to llm for response
  print("Sending payload to LLM API...")
  response = post(payload=articles)
  print("LLM response recieved.")
        
  #write to file
  print("Writing to file.")
  write(content=response, filename="summary.html")
  print("Done.")
  
run()
