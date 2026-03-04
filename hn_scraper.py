import requests
from bs4 import BeautifulSoup

def scrape(limit: int) -> list:
  '''Scrapes Hacker News and returns a list of articles'''

  # attempt to scrape HN
  print("Scraping..")
  try:
    soup = get_soup("https://news.ycombinator.com/")
    #HN uses html <span> elements with class="titlelines" as containers for article links
    titlelines = soup.find_all('span', class_="titleline", limit=limit)
  except:
    print("Failed to retrieve articles")
    return

  articles = []

  # get article title and weblink from html <a> anchor sub-elements
  for title in titlelines:
    a = title.find("a")
    
    # if no <a> element found give empty entry and continue to next article
    if not a:
      articles.append({title: None, url: None, "extracted_text": None})
      continue
    
    # otherwise grab link and title
    url = a.get("href")
    title = a.get_text(strip=True)
    
    # attempt to scrape weblink for article text
    try:
      soup = get_soup(url)
      body = soup.body
      extracted_text = body.get_text(" ", strip=True)
    except Exception as e:
      print(f"Failed to extract text: {e}")
      extracted_text = None
    
    articles.append({"title": title,"url": url, "extracted_text": extracted_text})
  
  print(f"Scraped {len(articles)} articles.")
  return articles

def get_soup(url):
  response = requests.get(url)
  response.raise_for_status()
  return BeautifulSoup(response.text, "html.parser")
  
