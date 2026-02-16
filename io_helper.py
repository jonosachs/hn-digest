from pathlib import Path
import json

def write(filename, content):
  '''Writes to file'''
  Path(filename).write_text(json.dumps(content, indent=2, ensure_ascii=False), encoding="utf-8")  

def read(filename):
  '''Reads from file'''
  return Path(filename).read_text(encoding="utf-8")
  
