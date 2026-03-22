import requests
from bs4 import BeautifulSoup

URL = "https://news.ycombinator.com/"
COMMENTS_URL = "https://news.ycombinator.com/item?id="

articles_inferred = 0 #counter for number of inferred summaries where article text couldn't be scraped

def scrape(limit: int = 5, get_comments_foreach: bool = False) -> dict:
  '''Scrapes Hacker News and returns a list of articles'''
    
  # attempt to scrape HN
  print("Scraping..")
  try:
    soup = get_soup(URL)
    # get html tablerows <tr> containing article metadata up to limit
    tablerows = soup.find_all('tr', class_="athing submission", limit=limit)
  except:
    print("Failed to retrieve articles")
    return

  articles = []

  for metadata in tablerows:
    # target html span tag should be in form:
    # <span class="titleline"><a href="https://www.usgs.gov/observatories/yvo/news/echinus-geyser-back-action-now">The largest acidic geyser has been putting on quite a show</a><span class="sitebit comhead"> (<a href="from?site=usgs.gov"><span class="sitestr">usgs.gov</span></a>)</span></span>
    a = metadata.find("span", class_="titleline").find("a")

    # if no <a> element found give empty entry and continue to next article
    if not a:
      articles.append({"title": None, "url": None, "text": None, "comments": None})
      continue
    
    article_url = a.get("href")
    article_title = a.get_text(strip=True)
    article_text = None
    article_comments = None
    
    # attempt to scrape weblink for article text
    try:
      soup = get_soup(article_url)
      body = soup.body
      article_text = body.get_text(" ", strip=True)[0:100_000] # cap at 100k chars
    # if this fails attempt to get article comments for context
    except Exception as e:
      print(f"Failed to extract text: {e}")
    
    if get_comments_foreach or not article_text:
      article_comments = get_comments(metadata)
    
    articles.append({"title": article_title,"url": article_url, "text": article_text, "comments": article_comments})
  
  print(f"Scraped {len(articles)-articles_inferred} articles.")
  print(f"Inferred {articles_inferred} articles.")
  return articles

def get_soup(url):
  response = requests.get(url)
  response.raise_for_status()
  return BeautifulSoup(response.text, "html.parser")
  
def get_comments(metadata):
  print("Getting article comments..")  
  
  global articles_inferred
  articles_inferred += 1
  
  article_id = metadata.get("id")
  comments_url = f"{COMMENTS_URL}{article_id}"
  
  try:
    soup = get_soup(comments_url)
    comments = [div.get_text("-----", strip=True) for div in soup.find_all("div", class_="commtext")]
    comments_capped = str(comments)[0:10_000]
    return comments_capped
  except Exception as e:
    print(f"Failed to extract comments: {e}")
    
