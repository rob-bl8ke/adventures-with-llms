# ticket-price-lookup.py — Walkthrough (Beginner Friendly)

This script builds a tiny “airline chat assistant” that can answer questions like:

- “How much is a ticket to Tokyo?”

It uses two key ideas:

1. A chat model (LLM) to talk to the user
2. A **tool/function** the model can call to look up ticket prices

It also uses **Gradio** to provide a simple web chat UI.

---

## What you need before running

### 1) A model endpoint

This script is currently configured to use **Ollama** (local) via an OpenAI-compatible API:

```py
MODEL = "llama3.2"
openai = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
```

That means:

- Ollama must be running locally
- The `llama3.2` model should be available in Ollama

If you want to use OpenAI instead, the script shows commented-out lines:

```py
# MODEL = "gpt-4o-mini"
# openai = OpenAI()
```

### 2) Environment variables

- The script loads `.env`:

```py
load_dotenv(override=True)
```

- It prints whether `OPENAI_API_KEY` exists. (This matters for OpenAI, not for Ollama.)

### 3) Python packages

- `openai`
- `python-dotenv`
- `gradio`

---

## Big picture: how tool calling works

Normally, an LLM only “predicts text”. It doesn’t *actually know* your ticket prices.

Tool calling solves this:

- You give the model a list of functions it is allowed to call.
- If the model needs real data, it can request a tool call.
- Your code runs the function and sends the result back to the model.
- Then the model writes a final response for the user.

This is how you connect an LLM to real-world data.

---

## Step-by-step: the code

### 1) Ticket price “database”

```py
ticket_prices = {
  "london": "$799",
  "paris": "$899",
  "tokyo": "$1400",
  "berlin": "$499"
}
```

This is just a Python dictionary: keys are city names, values are prices.

### 2) The tool function

```py
def get_ticket_price(destination_city):
    city = destination_city.lower()
    return ticket_prices.get(city, "Unknown")
```

This is a normal Python function.

- It lowercases the city name so “Tokyo” and “tokyo” match.
- If the city isn’t found, it returns `"Unknown"`.

### 3) Describe the tool to the model (schema)

```py
price_function = {
  "name": "get_ticket_price",
  "description": "...",
  "parameters": {
    "type": "object",
    "properties": {
      "destination_city": {"type": "string"}
    },
    "required": ["destination_city"],
    "additionalProperties": False
  }
}

tools = [{"type": "function", "function": price_function}]
```

This tells the model:

- The tool name it can call: `get_ticket_price`
- What the tool does
- What inputs it needs (`destination_city`)

Beginner note: this is similar to a JSON schema.

### 4) The chat handler

Gradio calls this function whenever the user sends a message:

```py
def chat(message, history):
    messages = ([{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}])

    response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)

    if response.choices[0].finish_reason == "tool_calls":
        ...

    return response.choices[0].message.content
```

What happens:

1. It builds up the conversation (system + previous messages + latest user message)
2. It calls the model, *including the `tools=` list*
3. If the model requests a tool call, we execute it
4. Then we call the model again so it can respond to the user with the tool result

### 5) Handling a tool call

```py
def handle_tool_call(message):
    tool_call = message.tool_calls[0]
    arguments = json.loads(tool_call.function.arguments)
    city = arguments.get("destination_city")

    price = get_ticket_price(city)

    response = {
        "role": "tool",
        "content": json.dumps({"destination_city": city, "price": price}),
        "tool_call_id": tool_call.id,
    }
    return response, city
```

Key pieces:

- `message.tool_calls[0]` contains the model’s requested function name + arguments.
- The model sends tool arguments as JSON, so we parse with `json.loads(...)`.
- We call our Python function to get the real price.
- We return a message with `role: "tool"` so the model can “see” the result.

### 6) Gradio UI

```py
gr.ChatInterface(fn=chat, type="messages").launch(inbrowser=True)
```

This starts a local web server and opens a browser tab where you can chat.

---

## Common issues and tips

- If you use Ollama: make sure it’s running and `llama3.2` is available.
- If the model doesn’t call the tool: sometimes you need to improve the system prompt (e.g., “Always call the tool when asked about prices”).
- Tool results are only as good as your data: right now it’s a tiny hard-coded dictionary.

---

## Easy experiments

- Add more cities to `ticket_prices`.
- Update the system message to enforce tool usage.
- Swap the model between Ollama and OpenAI.
- Allow multiple tools (e.g., `get_flight_duration`, `get_baggage_fee`).
