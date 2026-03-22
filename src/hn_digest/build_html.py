from pathlib import Path
from prompt import Articles

def build(content: dict):
  '''Builds structured HTML from LLM response'''
  
  print("Building HTML..")
  
  # create cards for each article
  cards = ""
  for article in content["articles"]:      
    if article['notes']:
      notes = f"<p>Notes: {article['notes']}</p>"
    else: 
      notes = ""
    
    cards += f"""
    <div class="card">
      <h2>{article['id']}. {article['title']}</h2>
      <p>URL: <a href={article['url']}>{article['url']}</a></p>
      <p>Confidence: {article['confidence']}</p>
      {notes}
      <p>Summary: {article['summary']}</p>
      <p>Significance: {article['significance']}</p>
      <p>Background: {article['background']}</p>
    </div>
    """

  # insert cards in HTML template body
  template = Path("./template.html").read_text(encoding="utf-8")
  
  print("Done.")
  return template.replace("{{CONTENT}}", cards)

