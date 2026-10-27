cat > README.md <<'EOF'
# Web Scraper

A web crawler I built while learning Python through Boot.dev.

The project started as a simple HTML scraper and gradually grew into an asynchronous crawler capable of visiting multiple pages concurrently.

## What it does

- Crawls pages within a given website.
- Extracts headings, paragraphs, links, and image URLs.
- Uses asyncio and aiohttp for concurrent requests.
- Avoids visiting the same URL multiple times.
- Supports configurable concurrency and page limits.
- Saves the collected data to a JSON report.

## Running it

Install dependencies:

    uv sync

Run the crawler:

    uv run main.py https://learnwebscraping.dev/practice/ecommerce/ 3 10

The last two arguments specify maximum concurrency and maximum pages.

## About

A guided Boot.dev project that helped me understand asynchronous Python, HTTP requests, HTML parsing, and concurrency.
EOF
