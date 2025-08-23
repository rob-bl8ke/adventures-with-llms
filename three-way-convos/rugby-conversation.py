import os
from dotenv import load_dotenv
from openai import OpenAI
import ollama
import anthropic
from IPython.display import Markdown, display, update_display

# Load environment variables
load_dotenv(override=True)

# Initializing API Clients, loading the SDKs
openai = OpenAI()
claude = anthropic.Anthropic()
ollama_via_openai = OpenAI(base_url='http://localhost:11434/v1', api_key = 'ollama')

# Conversation between GPT-4o-mini, Claude-3, ang Gemini 2.5 flash
bok_model = "gpt-4o-mini"
wallaby_model = "llama3.2"
allblack_model = "claude-3-haiku-20240307"

bok_system = "You are a Springbok rugby die-hard supporter. \
    You speak with a Pretoria accent and use typical colloquialisms, using South African rugby terminology. \
    Although you respect the game and its players, you are fiercely passionate about your opinions. \
    You see the New Zealand All Blacks as your biggest rivals and have strong feelings about their playing style. \
    You believe the Springbok playing style is superior and embodies the true spirit of rugby. \
    You can get defensive if anyone criticizes the Springboks or their playing style."

wallaby_system = "You are a Wallaby rugby die-hard supporter. \
    You speak with an Australian accent and use typical colloquialisms, using Australian rugby terminology. \
    Although you respect the game and its players, you are fiercely passionate about your opinions. \
    You believe your's is the best rugby team in the world and you thinks scrums and lineouts slow the game down. \
    In your loud opinion you think the Wallabies play the game with more flair and creativity. \
    You believe the Australian playing style is superior and embodies the true spirit of rugby. \
    You can become quite sarcastic and/or touchy when challenged about your team."

allblack_system = "You are an All Black rugby die-hard supporter. \
    You speak with a New Zealand accent and use typical colloquialisms, using New Zealand rugby terminology. \
    Although you respect the game and its players, you are fiercely passionate about your opinions. \
    You see the South African Springboks as your biggest rivals and have strong feelings about their playing style. \
    You believe the All Black playing style is superior and embodies the true spirit of rugby. \
    Your advantage is your wit, and quick tongue when challenged about your team."


bok_messages = ["Hey Ous. There is no doubt that the Springboks are the best rugby team in the world."]
wallaby_messages = ["Here we go again."]
allblack_messages = ["I'm all ears, mate."]

def get_bok_reply():
    
    messages = [{"role":"system", "content":bok_system}]
    
    for gpt, ollama, claude in zip(bok_messages, wallaby_messages, allblack_messages):
        messages.append({"role": "assistant", "content": gpt})
        messages.append({"role": "user", "content": ollama})
        messages.append({"role": "user", "content": claude})
    
    response = openai.chat.completions.create(
        model = bok_model,
        messages = messages,
        max_tokens = 500
    )
    return response.choices[0].message.content.strip()

def get_wallaby_reply():
    messages = [{"role":"system", "content":wallaby_system}]
    
    for gpt, ollama_message, claude in zip(bok_messages, wallaby_messages, allblack_messages):
        messages.append({"role": "user", "content": gpt})
        messages.append({"role": "assistant", "content": ollama_message})
        messages.append({"role": "user", "content": claude})
    
    messages.append({"role":"user", "content": bok_messages[-1]})

    response = ollama_via_openai.chat.completions.create(
            model = wallaby_model,
            messages = messages
    )
    return response.choices[0].message.content.strip()

def get_allblack_reply():
    
    messages = []
    
    for gpt, ollama, claude_message in zip(bok_messages, wallaby_messages, allblack_messages):
        messages.append({"role":"user", "content":gpt})
        messages.append({"role": "user", "content": ollama})
        messages.append({"role":"assistant", "content": claude_message})
    
    messages.append({"role": "user", "content": bok_messages[-1]})
    messages.append({"role": "user", "content": wallaby_messages[-1]})
    
    response = claude.messages.create(
        model = allblack_model,
        system = allblack_system,
        messages = messages,
        max_tokens = 500
    )
    return response.content[0].text.strip()

print(f"Frikkie (Springbok Supporter):\n{bok_messages[0]}\n")
print(f"James (Wallaby Supporter):\n{wallaby_messages[0]}\n")
print(f"Oliver (All Black Supporter):\n{allblack_messages[0]}\n")

for i in range(5):
    bok_reply = get_bok_reply()
    print(f"Frikkie (Springbok Supporter): \n{bok_reply}\n")
    bok_messages.append(bok_reply)

    wallaby_reply = get_wallaby_reply()
    print(f"James (Wallaby Supporter): \n{wallaby_reply}\n")
    wallaby_messages.append(wallaby_reply)

    allblack_reply = get_allblack_reply()
    print(f"Oliver (All Black Supporter): \n{allblack_reply}\n")
    allblack_messages.append(allblack_reply)