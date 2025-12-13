**Understanding Prompts**

* A prompt consists of two parts: a system prompt and a user prompt
* The system prompt is used by the LLM to generate tokens, while the user prompt is provided by the user to guide the LLM's output
* Both prompts should be clear and well-structured

**Why JSON and Markdown Work Well**

* Many LLMs are trained on large amounts of natural language text, markdown, and JSON data
* This training enables them to recognize and produce structured responses in these formats
* Using JSON for structured outputs can help the model generate coherent responses that meet user expectations

**Expressing Structured Information**

* Using JSON is a great way to express structured information, as it provides a clear and organized format for the LLM to work with
* This approach is more effective than trying to describe layouts using English bullets or other methods

**One-shot vs Multi-shot Prompting**

* One-shot prompting involves providing only one example to guide the LLM's output
* Multi-shot prompting involves providing multiple examples to help the LLM learn and improve over time
* In this tutorial, we are doing single-shot prompting by providing a single example prompt and then refining it through iteration

**Building the User Prompt and Fetching Links**

* The user prompt is generated based on the input URL and should guide the LLM to provide relevant links for a brochure about the company
* The system prompt is provided as a constant, while the user prompt is generated each time with a new URL
* Both prompts are then passed to the chat completions API using the OpenAI client library

**Making the First AI Call**

* The first AI call involves passing both the system and user prompts to the chat completions API
* The response format is set to JSON, which constrains the model's output to produce well-formed JSON responses
* The API call returns a list of dictionaries containing the LLM's output, which can be processed further

**Key Takeaways**

* Start by defining clear and well-structured prompts (system prompt and user prompt)
* Use JSON for structured outputs to enable coherent and organized responses
* Iterate on prompts through experimentation, refinement, and adding constraints (e.g., exclude privacy or terms links) to improve results
* Use the chat completions API with a model, messages, and response format (e.g., JSON) to constrain output and generate well-formed responses.