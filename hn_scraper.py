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
    hyperlink = title.find("a")
    link = hyperlink["href"]
    title = hyperlink.get_text(strip=True)
  
    try:
      soup = get_soup(link)
      body = soup.body
      extracted_text = body.get_text(" ", strip=True)
    except:
      extracted_text = ""
      print("Failed to extract text")
      
    articles.append({"title": title,"link": link, "extracted_text": extracted_text})
    
  return articles

def get_soup(url):
  response = requests.get(url)
  response.raise_for_status()
  return BeautifulSoup(response.text, "html.parser")
  
  
