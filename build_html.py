from pathlib import Path

def build(content: list[dict]):
  '''Builds structured HTML from LLM response'''
  
  # create cards for each article
  cards = ""
  for article in content:
    key_terms = article.get("key_terms", [])
    
    if key_terms:
      formatted_terms = ""
      for term in key_terms:
        formatted_terms += f"""
          <ul>
            <li>{term['term']} - {term['definition']}</li>
          </ul>
        """
    
    notext = "Text not available"
    
    if article['notes']:
      notes = f"<p>Notes: {article['notes']}</p>"
    else: 
      notes = "<span><span>"
    
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
  template = Path("template.html").read_text(encoding="utf-8")
  
  return template.replace("{{CONTENT}}", cards)

