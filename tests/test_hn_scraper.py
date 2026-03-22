import pytest
from hn_digest.hn_scraper import scrape
from hn_digest.io_helper import write

def test_scrape():
  # scrape articles
  content = scrape(limit=2, get_comments_foreach=True)

  # save to file for debugging (save to scraped_.txt to avoid race condition)
  write("./tests/write/scraped_.txt", content)

  assert content[0]['title'] is not None
  assert content[0]['url'] is not None
  
  
  
