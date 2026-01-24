# rugby-conversation.py — Walkthrough (Beginner Friendly)

This script makes **three different AI “characters” talk to each other** about rugby, each powered by a different model/provider:

- **Springbok fan** → OpenAI model (`gpt-4o-mini`)
- **Wallaby fan** → local Ollama model (`llama3.2`) *accessed through an OpenAI-compatible API*
- **All Black fan** → Anthropic Claude (`claude-3-haiku-20240307`)

The main idea is: keep a running chat history for each speaker, and repeatedly ask each model to generate its next reply.

---

## What you need before running

### 1) API keys / services

- OpenAI: set `OPENAI_API_KEY` in your environment (often via a `.env` file)
- Anthropic: you typically also need `ANTHROPIC_API_KEY` in your environment
- Ollama: you need Ollama running locally on your machine
  - This script assumes an OpenAI-style endpoint at `http://localhost:11434/v1`

### 2) Python packages

This script imports:

- `openai`
- `anthropic`
- `ollama` (imported, but not actually used in the code below)
- `python-dotenv`
- `IPython` display helpers (imported, but not actually used in the code below)

---

## Big picture: how the conversation works

There are three lists:

- `bok_messages` — everything the Springbok character has said so far
- `wallaby_messages` — everything the Wallaby character has said so far
- `allblack_messages` — everything the All Black character has said so far

The script starts each list with one “opening line”. Then it loops 5 times:

1. Generate the Springbok reply → append to `bok_messages`
2. Generate the Wallaby reply → append to `wallaby_messages`
3. Generate the All Black reply → append to `allblack_messages`

That’s it: **generate → print → remember**.

---

## Step-by-step: the code

### 1) Load environment variables

```py
load_dotenv(override=True)
```

This loads values from a `.env` file into your environment variables, so libraries like OpenAI/Anthropic can pick up your API keys.

### 2) Create “clients” (SDK objects)

```py
openai = OpenAI()
claude = anthropic.Anthropic()
ollama_via_openai = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
```

What each one means:

- `OpenAI()` creates a client that talks to OpenAI.
- `anthropic.Anthropic()` creates a client that talks to Claude.
- `OpenAI(base_url=...)` is a neat trick: it points the OpenAI client at a *different server*.
  - Ollama provides an API that looks like OpenAI’s, so the same client can be reused.

---

## Understanding the “system prompts”

Each character has a big string like:

- `bok_system`
- `wallaby_system`
- `allblack_system`

These are **system prompts**: instructions that describe personality, tone, and constraints.

Example (conceptually):

- “You are a die-hard Springbok supporter … speak with a Pretoria accent …”

This is how you turn a generic model into a “character”.

---

## The reply functions

### `get_bok_reply()` (OpenAI)

- Starts with a `messages` list containing a system message.
- Then it loops through the three histories using `zip(...)`.
- It builds a conversation for the Springbok model and calls:

```py
openai.chat.completions.create(model=bok_model, messages=messages, max_tokens=500)
```

Beginner note: in OpenAI chat format:

- `role="system"` sets behavior
- `role="user"` is the input
- `role="assistant"` is the model’s previous outputs

This function mixes roles to simulate “who said what”.

### `get_wallaby_reply()` (Ollama via OpenAI-style API)

This is very similar, but it calls:

```py
ollama_via_openai.chat.completions.create(model=wallaby_model, messages=messages)
```

So it’s using the OpenAI client, but sending requests to your local Ollama server.

### `get_allblack_reply()` (Anthropic)

Claude uses a slightly different API:

```py
claude.messages.create(model=..., system=..., messages=..., max_tokens=500)
```

Notice:

- System prompt is passed separately as `system=...`.
- The returned text is in `response.content[0].text`.

---

## The main loop

```py
for i in range(5):
    bok_reply = get_bok_reply()
    bok_messages.append(bok_reply)

    wallaby_reply = get_wallaby_reply()
    wallaby_messages.append(wallaby_reply)

    allblack_reply = get_allblack_reply()
    allblack_messages.append(allblack_reply)
```

This is the “engine” that keeps the conversation going.

---

## Things to be aware of (common beginner gotchas)

- **Imports not used**: `os`, `ollama`, and the IPython display imports aren’t actually used. That’s not harmful, just extra.
- **`zip(...)` truncates**: `zip(a, b, c)` stops at the shortest list. That’s fine here because the lists are kept the same length by appending each turn.
- **Role formatting matters**: If roles are mixed incorrectly, the models may respond weirdly (or act like they are the wrong character).
- **Cost / speed**: Each turn makes 3 model calls; 5 rounds means 15 calls total.

---

## Easy experiments

- Change the personalities in the `*_system` prompts.
- Change `range(5)` to more/less turns.
- Change models (e.g., use a different Claude or OpenAI model).
- Print the constructed `messages` list to understand what each model is seeing.
