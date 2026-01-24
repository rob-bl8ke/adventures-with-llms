# scraper.py — Walkthrough (Beginner Friendly)

This file contains two helper functions used by the website scraping examples:

- `fetch_website_contents(url)` — download a page and return readable text
- `fetch_website_links(url)` — download a page and return the links (`href`s)

It uses:

- `requests` to download the HTML
- `beautifulsoup4` (BeautifulSoup) to parse and extract data from HTML

---

## Why this helper exists

Raw HTML is messy. LLMs (and humans) do better when you provide:

- mostly-visible text (not scripts/styles)
- a reasonable size limit (so prompts don’t get huge)

This scraper tries to do “just enough cleaning” for a learning project.

---

## Code walkthrough

### 1) Imports

```py
from bs4 import BeautifulSoup
import requests
```

- `requests.get(...)` downloads a web page.
- `BeautifulSoup(...)` parses the HTML into something you can query.

### 2) A User-Agent header

```py
headers = {
  "User-Agent": "Mozilla/5.0 ..."
}
```

Many websites treat requests differently depending on the User-Agent.

Using a browser-like User-Agent helps avoid some basic blocks (though it’s not a guarantee).

---

## `fetch_website_contents(url)`

### What it returns

A single string containing:

- the page title
- the visible page text

It truncates to 2,000 characters.

### How it works

1. Download the HTML:

```py
response = requests.get(url, headers=headers)
```

2. Parse HTML:

```py
soup = BeautifulSoup(response.content, "html.parser")
```

3. Read the `<title>` (if present)

4. If there is a `<body>`:

- remove elements that usually aren’t useful for summarization:

```py
for irrelevant in soup.body(["script", "style", "img", "input"]):
    irrelevant.decompose()
```

- get the remaining text:

```py
text = soup.body.get_text(separator="\n", strip=True)
```

5. Return `(title + "\n\n" + text)[:2_000]`

### Why remove `script/style/img/input`?

- `script` and `style` are not “content”
- `img` has no visible text (usually)
- `input` is often form UI

Removing them reduces noise.

---

## `fetch_website_links(url)`

### What it returns

A list of link targets from the page, e.g.:

- `"/about"`
- `"https://example.com/careers"`

### How it works

1. Download + parse HTML
2. Find all anchor tags:

```py
soup.find_all("a")
```

3. Extract the `href` attribute:

```py
links = [link.get("href") for link in soup.find_all("a")]
```

4. Filter out `None` values:

```py
return [link for link in links if link]
```

### Beginner gotcha: relative URLs

Many `href`s are relative (like `/about`). If you later try `requests.get("/about")`, it will fail.

Usually you fix this by converting relative links to absolute ones using `urllib.parse.urljoin(base_url, href)`.

---

## Practical tips

- Add timeouts: `requests.get(url, ..., timeout=10)`
- Handle errors: check `response.status_code` or wrap in `try/except`
- Some sites require JavaScript rendering: `requests` won’t execute JS, so you may need a browser automation tool for those sites.
