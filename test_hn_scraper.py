import pytest
from hn_scraper import scrape
from io_helper import write


def test_scrape():
  # scrape articles
  content = scrape(limit=2)

  # save to file for debugging (save to scraped_.txt to avoid race condition)
  write("./test/scraped_.txt", content)

  assert content[0]['title'] is not None
  assert content[1]['url'] is not None
  
  
  
