# scraper.py — Walkthrough (Beginner Friendly)

This file contains the web scraping helpers used by the brochure generator:

- `fetch_website_links(url)` — collect all links from a page
- `fetch_website_contents(url)` — collect readable text from a page

It’s the “data gathering” part of the pipeline. The LLM parts happen in `sales-brochure-generator.py`.

---

## What you need before running

### Python packages

- `requests`
- `beautifulsoup4`

---

## How scraping works here (plain English)

A website is sent to you as HTML (markup). This scraper:

- downloads the HTML
- parses it into a tree of elements
- extracts either:
  - link URLs (`href` attributes)
  - visible-ish text from the page body

---

## Code walkthrough

### 1) Imports

```py
from bs4 import BeautifulSoup
import requests
```

### 2) Browser-like headers

```py
headers = {
  "User-Agent": "Mozilla/5.0 ..."
}
```

This can help some sites treat your request like a real browser.

---

## `fetch_website_contents(url)`

### Goal

Return a string that’s useful to feed into an LLM prompt:

- the page title
- the main text content
- capped at 2,000 characters

### Key steps

1. Download:

```py
response = requests.get(url, headers=headers)
```

2. Parse HTML:

```py
soup = BeautifulSoup(response.content, "html.parser")
```

3. Extract title:

```py
title = soup.title.string if soup.title else "No title found"
```

4. If `<body>` exists, delete noisy nodes:

```py
for irrelevant in soup.body(["script", "style", "img", "input"]):
    irrelevant.decompose()
```

5. Extract text:

```py
text = soup.body.get_text(separator="\n", strip=True)
```

6. Return:

```py
(title + "\n\n" + text)[:2_000]
```

### Why the 2,000 character limit?

Brochure prompts can get expensive quickly. Limiting the amount of text per page helps keep:

- prompt size smaller
- costs lower
- responses faster

---

## `fetch_website_links(url)`

### Goal

Return all links found on the page.

### Key steps

- Download + parse HTML
- Get all `<a>` tags
- Pull out `href`

```py
links = [link.get("href") for link in soup.find_all("a")]
return [link for link in links if link]
```

### Beginner gotcha: relative links

Many links are relative (like `/about`). For the brochure generator, you generally want full URLs.

A common improvement is:

- `from urllib.parse import urljoin`
- `absolute = urljoin(base_url, href)`

---

## Practical tips (if you want to improve it later)

- Add `timeout=...` to `requests.get`.
- Handle non-200 responses.
- Deduplicate links and filter out mailto/tel/javascript links.
- Cache results so you don’t download the same page multiple times.
