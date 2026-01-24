# website-scrape.py — Walkthrough (Beginner Friendly)

This script scrapes the text content of a website and asks an LLM to produce a short, snarky summary.

It demonstrates a very common pattern:

1. Download a web page
2. Extract readable text
3. Send that text to an LLM with instructions (a prompt)
4. Print the LLM’s summary

---

## Files involved

- `website-scrape.py`
  - Orchestrates the scrape + summarize flow
- `scraper.py`
  - Provides `fetch_website_contents(url)` (HTML → readable text)

---

## What you need before running

### 1) API key

This script expects an OpenAI key in an environment variable:

- `OPENAI_API_KEY`

It loads it from a `.env` file *one level above this folder*:

```py
load_dotenv(dotenv_path="../.env", override=True)
```

That means it’s looking for:

- `adventures-with-llms/.env`

### 2) Python packages

- `openai`
- `python-dotenv`
- `requests` and `beautifulsoup4` (used by `scraper.py`)

---

## Step-by-step: the code

### 1) Load environment variables and read the API key

```py
load_dotenv(dotenv_path="../.env", override=True)
api_key = os.getenv("OPENAI_API_KEY")
```

- `load_dotenv(...)` reads a `.env` file and puts values into the environment.
- `os.getenv(...)` retrieves one value from the environment.

### 2) Validate the key (helpful beginner checks)

The script prints helpful messages if:

- No key exists
- The key doesn’t start with `sk-proj-`
- The key has leading/trailing whitespace

These checks are just “guard rails” so you don’t waste time debugging authentication.

### 3) Create an OpenAI client

```py
openai = OpenAI()
```

The OpenAI SDK will typically read your key from `OPENAI_API_KEY` automatically.

### 4) Define prompts

Two prompts are used:

#### System prompt

```py
system_prompt = """
You are a snarky assistant ...
Respond in markdown ...
"""
```

A system prompt sets behavior and style.

#### User prompt prefix

```py
user_prompt_prefix = """
Here are the contents of a website...
"""
```

This is the “task” plus instructions for what to summarize.

### 5) Build messages for the chat model

```py
def messages_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_prefix + website},
    ]
```

This creates the list of messages that will be sent to the model.

Beginner note: chat models take a conversation as a list of messages, each with:

- `role`: system/user/assistant
- `content`: text

### 6) Scrape + summarize

```py
def summarize(url):
    website = fetch_website_contents(url)
    response = openai.chat.completions.create(
        model="gpt-4.1-mini", messages=messages_for(website)
    )
    return response.choices[0].message.content
```

What happens here:

1. `fetch_website_contents(url)` downloads the page and extracts visible text
2. That text is appended to the user message
3. The script calls the model (`gpt-4.1-mini`)
4. It returns the model’s summary text

### 7) Print the result

```py
display_summary("https://cnn.com")
```

This prints the LLM’s summary to the terminal.

---

## What `fetch_website_contents` is doing (in plain English)

Although it lives in `scraper.py`, conceptually it:

- downloads HTML (`requests.get`)
- removes noisy parts like scripts/styles/images
- extracts text from the page body
- truncates to a reasonable size

This gives the LLM something closer to “article text” instead of raw HTML.

---

## Common issues and tips

- Some sites block scraping: you might get a 403 or a different HTML page than expected.
- Many modern sites are JavaScript-heavy: the HTML you download might not contain the content you see in a browser.
- If summaries look bad, try:
  - using a different URL
  - adjusting the system prompt (tone)
  - increasing/decreasing how much content `fetch_website_contents` returns

---

## Easy experiments

- Change the system prompt to be serious instead of snarky.
- Change the output language (“Respond in markdown in Spanish.”).
- Summarize a different site.
- Print the scraped `website` text to see what the model is actually receiving.
