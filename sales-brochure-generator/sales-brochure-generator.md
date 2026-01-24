# sales-brochure-generator.py — Walkthrough (Beginner Friendly)

This script generates a short “sales brochure” for a company by:

1. Scraping a company’s website for links and page text
2. Asking an LLM (a chat model) which links look relevant (About/Careers/etc.)
3. Scraping those relevant pages too
4. Asking an LLM to write a brochure in Markdown based on the scraped content

It’s a simple example of **LLM + web scraping + prompting**.

---

## Files involved

- `sales-brochure-generator.py`
  - Orchestrates the whole flow (scrape → choose links → scrape more → write brochure)
- `scraper.py`
  - Contains the web-scraping helper functions using `requests` + `BeautifulSoup`

---

## What you need before running

### 1) Python packages

The script relies on packages like:

- `openai` (to call the OpenAI chat models)
- `python-dotenv` (so you can store secrets in a `.env` file)
- `requests` + `beautifulsoup4` (to download and parse HTML)

### 2) Your API key

It expects an environment variable:

- `OPENAI_API_KEY`

Common setup:

- Create a `.env` file (for example in the repo root) with:

```text
OPENAI_API_KEY=your_key_here
```

Then the code runs `load_dotenv(override=True)` to load that `.env` into your process environment.

---

## High-level flow (mental model)

Think of the program as two phases:

### Phase A — “Research” (LLM helps pick which pages matter)

1. Download the landing page HTML
2. Extract all `<a href="...">` links
3. Send the list of links to an LLM
4. The LLM returns a JSON list like:

```json
{
  "links": [
    {"type": "about page", "url": "https://example.com/about"},
    {"type": "careers page", "url": "https://example.com/careers"}
  ]
}
```

### Phase B — “Write the brochure” (LLM writes from scraped text)

1. Download the landing page text
2. Download the text of each “relevant” link
3. Concatenate the text into one big prompt
4. Ask an LLM to write the brochure in Markdown

---

## Step-by-step: `sales-brochure-generator.py`

### 1) Imports

```py
import os
import json
from dotenv import load_dotenv
from scraper import fetch_website_links, fetch_website_contents
from openai import OpenAI
```

- `os` lets you read environment variables like `OPENAI_API_KEY`.
- `json` parses the JSON string returned by the LLM.
- `load_dotenv` loads variables from a `.env` file.
- `fetch_website_links` and `fetch_website_contents` come from your local `scraper.py`.
- `OpenAI` is the client used to call chat models.

### 2) Load `.env` and configure the client

```py
load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")

MODEL = "gpt-5-nano"
openai = OpenAI()
```

Important notes:

- `api_key` is read but not directly used later. That’s okay because the `openai` client will typically read `OPENAI_API_KEY` from the environment.
- `MODEL` is used for the link-selection step.

### 3) Prompt for link selection

The script defines a **system prompt** named `link_system_prompt`.

A *system prompt* is instructions that set the assistant’s behavior. Here, it says:

- You will get a list of links
- Pick the ones relevant for a brochure (About, Careers, etc.)
- Respond with a specific JSON structure

This is a classic pattern:

- **System prompt**: strict instructions
- **User prompt**: the actual input (the website’s links)

### 4) Build the user prompt with real scraped links

```py
def get_links_user_prompt(url):
    links = fetch_website_links(url)
    user_prompt = "..." + "\n".join(links)
    return user_prompt
```

This function:

1. Calls `fetch_website_links(url)` (scraping)
2. Appends those links to a prompt string

### 5) Call the LLM to pick relevant links (JSON-only)

```py
def select_relevant_links(url):
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": link_system_prompt},
            {"role": "user", "content": get_links_user_prompt(url)},
        ],
        response_format={"type": "json_object"},
    )
    result = response.choices[0].message.content
    links = json.loads(result)
    return links
```

What’s happening here:

- `messages=[...]` is how you feed a conversation to the model.
- `response_format={"type": "json_object"}` tells the model it must output valid JSON.
- The result is parsed using `json.loads(...)` into a Python dictionary.

Why JSON-only output is useful:

- It makes the LLM easier to integrate into automation.
- You can reliably parse the response without guessing.

### 6) Scrape content for the landing page + the selected links

```py
def fetch_page_and_all_relevant_links(url):
    contents = fetch_website_contents(url)
    relevant_links = select_relevant_links(url)
    result = f"## Landing Page:\n\n{contents}\n## Relevant Links:\n"

    for link in relevant_links["links"]:
        result += f"\n\n### Link: {link['type']}\n"
        result += fetch_website_contents(link["url"])

    return result
```

This function:

1. Gets the landing page text
2. Uses the LLM to decide “which links matter”
3. Downloads and appends the text from those chosen pages

So the brochure model later gets a mini “research dossier”.

### 7) Prompt for brochure writing

`brochure_system_prompt` tells the model to:

- Analyze the scraped pages
- Write a short brochure
- Output Markdown (but *without code blocks*)
- Include culture/customers/careers if possible

There’s also a commented-out “serious” version and an active “humorous” version.

This is an important prompting concept:

- **Tone is just instructions.** You can change style without changing code logic.

### 8) Build the brochure user prompt (with truncation)

```py
def get_brochure_user_prompt(company_name, url):
    user_prompt = f"You are looking at a company called: {company_name} ..."
    user_prompt += fetch_page_and_all_relevant_links(url)
    user_prompt = user_prompt[:5_000]
    return user_prompt
```

Key idea: **truncation**.

- LLM input size affects cost and sometimes latency.
- This script slices the prompt to 5,000 characters to control cost.
- Tradeoff: you might cut off useful info.

### 9) Call the LLM to write the brochure

```py
def create_brochure(company_name, url):
    response = openai.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": brochure_system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(company_name, url)},
        ],
    )
    return response.choices[0].message.content
```

Notice it uses a different model for writing (`gpt-4.1-mini`) than for link selection (`gpt-5-nano`).

Why you might do that:

- One model might be cheaper/faster for structured link selection
- Another might be better at writing fluent marketing copy

### 10) Run it

```py
print(create_brochure("HuggingFace", "https://huggingface.co"))
```

This prints the final brochure Markdown to the terminal.

---

## Step-by-step: `scraper.py`

### `fetch_website_links(url)`

- Downloads the HTML with `requests.get`
- Parses it with BeautifulSoup
- Finds all anchor tags: `soup.find_all("a")`
- Extracts the `href` attribute

Output: a list like `['/about', 'https://example.com/careers', ...]`.

Note: some links may be **relative** (like `/about`). That can be a problem if you later try to fetch them directly as URLs.

### `fetch_website_contents(url)`

- Downloads the HTML
- Removes some noisy elements: `script`, `style`, `img`, `input`
- Pulls visible text from the page
- Returns a string of up to 2,000 characters

This function tries to give the LLM “mostly readable text” instead of raw HTML.

---

## Key LLM concepts used here (plain English)

- **Prompting**: You’re writing instructions + supplying content.
- **System vs user messages**:
  - *System*: rules/behavior
  - *User*: the task + the data
- **Structured outputs (JSON)**: You constrain the LLM’s response so code can parse it.
- **Token/cost control**: truncation reduces how much text you send.

---

## Common issues and tips

- **Relative links**: If the model returns `/about`, `requests.get('/about')` won’t work. You typically need to convert relative links to full URLs.
- **Sites block scraping**: Some websites will reject requests or require JavaScript rendering.
- **Prompt truncation**: If the brochure looks incomplete, increase the truncation limit (while watching cost).
- **API key not found**: If you get authentication errors, confirm `OPENAI_API_KEY` is set.

---

## Easy experiments you can try

- Change tone: edit `brochure_system_prompt` to be serious vs funny.
- Change the link selection rules: tell it to prefer Product/Pricing pages.
- Try a different company URL.
- Print out `relevant_links` so you can see which pages the LLM selected.