from pathlib import Path

def build(content: list[dict]):
  #create cards for each article
  cards = ""
  
  for entry in content:
    formatted_terms = ""
    key_terms = entry["key_terms"]
    
    for term in key_terms:
      formatted_terms += f"""
        <ul>
          <li>{term['term']} - {term['definition']}</li>
        </ul>
      """
    
    fail = "Text not available"
    
    cards += f"""
    <div class="card">
      <h2>{entry['id']}. {entry['title'] or fail}</h2>
      <p>URL: <a href={entry['url']}>{entry['url']}</a></p>
      <p>Summary: {entry['summary']}</p>
      <p>Key Terms: {formatted_terms or fail}</p>
      <p>Significance: {entry['why_it_matters']}</p>
      <p>Confidence: {entry['confidence']}</p>
      <p>Notes: {entry['notes']}</p>
    </div>
    """

  #insert place cards within HTML template
  template = Path("template.html").read_text(encoding="utf-8")
  return template.replace("{{CONTENT}}", cards)

