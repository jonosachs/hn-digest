from pathlib import Path
import json

def write(filename, content):
  '''Writes to file'''
  path = Path(filename)
  path.parent.mkdir(parents=True, exist_ok=True)
  
  if isinstance(content, (dict, list)):
    path.write_text(json.dumps(content, indent=2, ensure_ascii=False), encoding="utf-8")
  else:
    path.write_text(content, encoding="utf-8")

def read(filename):
  '''Reads from file'''
  content = Path(filename).read_text(encoding="utf-8")
  try:
    return json.loads(content)
  except json.JSONDecodeError:
    return content
  
