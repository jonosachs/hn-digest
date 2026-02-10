import requests
from bs4 import BeautifulSoup

def scrape(limit):
  try:
    soup = get_soup("https://news.ycombinator.com/")
    titlelines = soup.find_all('span', class_="titleline", limit=limit)
  except:
    print("Failed to retrieve articles")
    return

  articles = []

  for title in titlelines:
    a = title.find("a")
    
    if not a:
      articles.append({title: None, link: None, "extracted_text": None})
      continue
    
    link = a.get("href")
    title = a.get_text(strip=True)
    extracted_text = None
    
    try:
      soup = get_soup(link)
      body = soup.body
      extracted_text = body.get_text(" ", strip=True)
    except Exception as e:
      print(f"Failed to extract text: {e}")
    
    articles.append({"title": title,"link": link, "extracted_text": extracted_text})
    
  return articles

def get_soup(url):
  response = requests.get(url)
  response.raise_for_status()
  return BeautifulSoup(response.text, "html.parser")
  
