# HN Digest 🗞️

Generate a daily HTML digest of the latest Hacker News posts using Gemini for summaries and background context, delivered straight to your inbox.

## What it does

- Scrapes the top Hacker News titles, article text, and reader comments
- Sends the articles to Gemini for summaries, significance, and background context (using structured JSON output)
- Builds an HTML report and emails it to you
- Runs automatically via GitHub Actions (daily at 9 AM UTC)

## Example article summary

```text
2. DuckDB Internals: Why Is DuckDB Fast? (Part 1)

URL: https://www.greybeam.ai/blog/duckdb-internals-part-1

Confidence: high

Summary: DuckDB is an analytical database designed to run 'in-process,' meaning it functions as a library within an application rather than a standalone server. This architecture eliminates the overhead of network serialization and communication protocols. DuckDB achieves high performance through columnar storage, which stores data for each column together, and vectorized execution, which processes batches of data at once to maximize CPU efficiency. It also uses 'zone maps' (min/max metadata) to skip irrelevant data blocks during scans.

Significance: DuckDB proves that a single-node, in-process engine can outperform massive database clusters for analytical workloads by focusing on architectural efficiency and zero-copy data sharing.

Background: In a traditional 'server-client' database model, the database is a separate program. When you request data, the server must 'serialize' the results—convert them from their internal memory format into a stream of bytes (a wire protocol)—to send them over a network. Your application then 'deserializes' those bytes back into local data types. This process is slow and consumes significant CPU cycles. DuckDB is an 'in-process' database, meaning it is a 'library' (a reusable piece of code) that you link directly into your software. Because they share the same memory space, DuckDB can use 'zero-copy' techniques, reading data directly from your application's memory without moving it. Databases generally use one of two storage layouts. A 'row store' keeps all data for one record (e.g., a user's ID, name, and age) next to each other. This is fast for looking up one person but slow for analysis. A 'column store' keeps all values for a single column (e.g., every user's age) together. For analytical queries that calculate averages or sums across millions of rows, columnar storage is much faster because the CPU only has to read the specific columns it needs from disk. To further speed up queries, DuckDB uses 'zone maps' and 'vectorized execution.' A 'zone map' is a summary of a block of data that stores the minimum and maximum values within it; if a query looks for values greater than 100 and the zone map says the max is 50, the database skips that block entirely. 'Vectorized execution' means the CPU processes data in 'vectors' (small batches) rather than one row at a time, which allows the chip to stay in a high-speed loop and reduces the number of function calls the program has to make.
```


## Requirements

- Python 3.9+
- A Gemini API key
- A Gmail account with an App Password for sending emails

## Setup

1. Create and activate a virtual environment (optional but recommended).
2. Install the package and dependencies:

```bash
pip install -e .
```

3. Create a `.env` file in the project root:

```bash
GEMINI_API_KEY=your_api_key_here
EMAIL_ADD=your_email@gmail.com
GOOGLE_APP_PASS=your_google_app_password
```

To generate a Google App Password, go to your Google Account > Security > 2-Step Verification > App passwords.

## Run locally

```bash
hn-digest
```

This will scrape HN, generate summaries, and email the digest to the configured address.

## GitHub Actions (automated daily digest)

The included workflow (`.github/workflows/send_email.yml`) runs the script daily at 9 AM UTC.

To enable it:

1. Fork or push this repo to GitHub.
2. Go to Settings > Secrets and variables > Actions.
3. Add the following repository secrets:
   - `GEMINI_API_KEY`
   - `EMAIL_ADD`
   - `GOOGLE_APP_PASS`

You can also trigger the workflow manually from the Actions tab.

## Configuration

- Edit `src/hn_digest/main.py` to change the number of articles (`scrape(limit=...)`).
- Update `src/hn_digest/prompt.py` to adjust the summarization instructions.
- Edit `src/hn_digest/templates/template.html` to change the report layout.

## Testing

Run the unit tests with pytest:

```bash
pytest -s
```

Tests cover LLM API response parsing and retry behaviour, HTML report generation, HN scraping, and email sending.

## Error handling

- **Fail-fast startup checks**: Before scraping or calling the LLM, the app validates that all credentials are present, the Gemini API connection is reachable, and the email login succeeds. This avoids wasting time and token limits on a run that would fail later.
- **LLM retry with backoff**: If the Gemini API returns a 429 (rate limit) error or a malformed JSON response, the call is automatically retried (up to 3 attempts) with a short delay.

## Notes

- If an article's body can't be extracted, reader comments are used as a fallback source. If neither is available, the summary is inferred from the title.
- Network access is required to scrape HN and call Gemini.

#README generated using Claude CLI
