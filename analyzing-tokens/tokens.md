# tokens.py — Walkthrough (Beginner Friendly)

This script is a tiny demo of **tokenization**.

Tokenization is how LLMs turn text into numbers (“tokens”) before processing it. Models don’t directly read raw strings — they operate on sequences of token IDs.

---

## What you need before running

### Python package

- `tiktoken`

This is OpenAI’s tokenizer library (it knows how certain OpenAI-model tokenizers break text into tokens).

---

## What the code does, step by step

### 1) Import the tokenizer library

```py
import tiktoken
```

### 2) Choose an encoding (tokenizer) that matches a model

```py
encoding = tiktoken.encoding_for_model("gpt-4.1-mini")
```

Different model families can have different tokenization rules.

`encoding_for_model(...)` picks an encoding that matches how that model expects text to be tokenized.

### 3) Convert text → token IDs

```py
tokens = encoding.encode("Hi my name is Andrew and I am a Hippopotamus")
```

- `encode(...)` returns a Python list of integers.
- Each integer is a token ID.

Then:

```py
print(tokens)
```

prints the full list of IDs.

### 4) Convert token IDs → text (one token at a time)

```py
for token_id in tokens:
    token_text = encoding.decode([token_id])
    print(f"{token_id} = {token_text}")
```

A few important beginner notes:

- `decode(...)` expects a *list* of token IDs, even if it’s just one token.
- A “token” is not always a whole word.
  - Sometimes it’s a piece of a word (like `"Hippo"` + `"potamus"`)
  - Sometimes it’s a space plus a word (like `" Andrew"`)

So this loop shows you exactly how the text is broken up.

### 5) Decode one specific token ID

```py
print(encoding.decode([326]))
```

This is just a quick example of: “what text does token 326 represent in this encoding?”

---

## Why tokenization matters (LLM basics)

- **Pricing / cost**: many APIs charge based on number of tokens, not characters.
- **Context limits**: models have a max number of tokens they can read at once.
- **Prompt design**: knowing token counts helps you keep prompts efficient.

---

## Easy experiments

- Replace the sentence with your own and see how tokens change.
- Try a sentence with emojis, punctuation, or another language.
- Print `len(tokens)` to see how many tokens your sentence uses.
