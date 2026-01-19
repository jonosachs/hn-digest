# HN Digest

Generate a simple HTML digest of the latest Hacker News posts using Gemini for summaries and key terms.

## What it does
- Scrapes the top Hacker News titles and article text
- Sends the articles to Gemini for summaries and key terms
- Writes an HTML report to `summary.html` and raw JSON to `raw.txt`

## Requirements
- Python 3.9+
- A Gemini API key

## Setup
1) Create and activate a virtual environment (optional but recommended).
2) Install dependencies:

```bash
pip install -r requirements.txt
```

3) Create a `.env` file in the project root:

```bash
GEMINI_API_KEY=your_api_key_here
```

## Run
```bash
python main.py
```

Outputs:
- `summary.html` — rendered digest
- `raw.txt` — JSON response from the model

## Configuration
- Edit `main.py` to change the number of articles (`scrape(limit=...)`).
- Update `prompt.py` to adjust the summarization instructions.
- Edit `template.html` to change the report layout.

## Notes
- If an article’s body can’t be extracted, the summary is inferred from the title.
- Network access is required to scrape HN and call Gemini.
