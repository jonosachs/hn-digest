from pathlib import Path
import json

def write(content, filename):
  Path("raw.txt").write_text(json.dumps(content, indent=2), encoding="utf-8")
  
  formatted = format(content)
  template = Path("template.html").read_text(encoding="utf-8")
  output = template.replace("{{CONTENT}}", formatted)
  Path(filename).write_text(output, encoding="utf-8")
  
def format(content):
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
    
    cards += f"""
    <div class="card">
      <h2>{entry['id']}. {entry['title']}</h2>
      <p>URL: <a href={entry['url']}>{entry['url']}</a></p>
      <p>Summary: {entry['summary']}</p>
      <p>Key Terms: {formatted_terms}</p>
      <p>Significance: {entry['why_it_matters']}</p>
      <p>Confidence: {entry['confidence']}</p>
      <p>Notes: {entry['notes']}</p>
    </div>
    """
    
  return cards