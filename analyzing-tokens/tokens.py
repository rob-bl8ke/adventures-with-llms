import tiktoken

# Fun with tokenization
encoding = tiktoken.encoding_for_model("gpt-4.1-mini")
tokens = encoding.encode("Hi my name is Andrew and I am a Hippopotamus")

# Prints out the tokens for this sententce
print(tokens)

# Decode the tokens
for token_id in tokens:
    token_text = encoding.decode([token_id])
    print(f"{token_id} = {token_text}")

# Decode a single token
print(encoding.decode([326]))
