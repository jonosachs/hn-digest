from pydantic import BaseModel, Field
from typing import List, Optional

CONTEXT = '''
  You are a technical editor.

  Task:
  Summarise a set of Hacker News articles. You will be given a list of articles, each with:
  - title
  - url
  - optional: extracted_text (may be empty)

  For EACH article, produce:
  1) A clear, succinct summary (1-2 paragraph) written for a Computer Science student as the intended audience. Technical concepts should be explained from first-principles.
  2) Key technical terms: list any technical terms that appear in the article (or are essential to understand it) with one-line definitions each.
  3) Why it matters: 1–2 sentences explaining why the findings are important, noteworthy, or relevant.

  Rules:
  - Use only the information provided in the input. If the article content is missing, base your output on the title + any snippets, and clearly state that the summary is inferred.
  - Do not invent facts, numbers, quotes, or claims not supported by the provided text/snippets.
  - Prefer concrete explanations over hype. Keep it concise.
  - If the article is non-technical, still provide a brief summary and define any domain-specific terms.

  Output format:
  Return valid JSON only (no markdown) matching the provided schema.

  Now process these articles:'''
  

class Term(BaseModel):
  term: str
  definition: str = Field(description="one liner")

class Entry(BaseModel):
  id: int = Field(description="Sequential, unique article number")
  title: str 
  url: str
  confidence: str = Field(description="high|medium|low")
  notes: Optional[str] = Field(description="e.g. Summary inferred from title only")
  summary: str = Field(description="Short paragraph summarising the article")
  key_terms: List[Term]
  why_it_matters: str = Field(description="1-2 sentences")

class Articles(BaseModel):
  articles: List[Entry]