from pathlib import Path
from prompt import Articles

def build(content: dict):
  '''Builds structured HTML from LLM response'''
  
  print("Building HTML..")
  
  # create cards for each article
  cards = ""
  for article in content["articles"]:    
    key_terms = article.get("key_terms", [])
    
    formatted_terms = ""
    
    if key_terms:
      formatted_terms += "<ul>"
      for term in key_terms:
        formatted_terms += f"<li>{term['term']} - {term['definition']}</li>"
      formatted_terms += "</ul>"
    
    notext = "Text not available"
    
    if article['notes']:
      notes = f"<p>Notes: {article['notes']}</p>"
    else: 
      notes = ""
    
    cards += f"""
    <div class="card">
      <h2>{article['id']}. {article['title'] or notext}</h2>
      <p>URL: <a href={article['url']}>{article['url']}</a></p>
      <p>Confidence: {article['confidence']}</p>
      {notes}
      <p>Summary: {article['summary']}</p>
      <p>Significance: {article['why_it_matters']}</p>
      <p>Key Terms: {formatted_terms or notext}</p>
    </div>
    """

  # insert cards in HTML template body
  template = Path("./template.html").read_text(encoding="utf-8")
  
  print("Done.")
  return template.replace("{{CONTENT}}", cards)

