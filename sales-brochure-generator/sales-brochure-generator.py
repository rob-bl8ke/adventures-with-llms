import os
import json
from dotenv import load_dotenv
from scraper import fetch_website_links, fetch_website_contents
from openai import OpenAI

# ##############################################################################
# Use on-shot prompting to make a company brochure... start with compiling info.
# ##############################################################################

# Initialize and constants
load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")

MODEL = "gpt-5-nano"
openai = OpenAI()

# System Prompt: This is always the same so it is a simple variable.
link_system_prompt = """
You are provided with a list of links found on a webpage.
You are able to decide which of the links would be most relevant to include in a brochure about the company,
such as links to an About page, or a Company page, or Careers/Jobs pages.
You should respond in JSON as in this example:

{
    "links": [
        {"type": "about page", "url": "https://full.url/goes/here/about"},
        {"type": "careers page", "url": "https://another.full.url/careers"}
    ]
}
"""


# User Prompt: Will change with different input, so it a function.
# The user prompt consists of thee main operations
# - The user's request
# - The call to a scraper that goes and fetches links
# - Concatenates the links to the end of the user prompt
def get_links_user_prompt(url):
    user_prompt = f"""
Here is the list of links on the website {url} -
Please decide which of these are relevant web links for a brochure about the company, 
respond with the full https URL in JSON format.
Do not include Terms of Service, Privacy, email links.

Links (some might be relative links):

"""
    links = fetch_website_links(url)
    user_prompt += "\n".join(links)
    return user_prompt


# Now make the call to the LLM using the messages derived from the
# above functions.
# - Restrict the LLM to responding to JSON (system prompt and format)
#   - This constains the "next most probable" token so that it must
#     be a valid JSON token.
# - Execute and load as JSON.
def select_relevant_links(url):
    # print(f"Selecting relevant links for {url} by calling {MODEL}")
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
    # print(f"Found {len(links['links'])} relevant links")
    return links


# print(select_relevant_links("https://huggingface.co"))

# ##############################################################################
# Now lets use this information to create a company brochure.
#   - For each link found, we're going to pull the information and the contents.
# ##############################################################################


# Fetch the contents for website and just append it all together to get a whole
# bunch of content.
def fetch_page_and_all_relevant_links(url):
    contents = fetch_website_contents(url)
    relevant_links = select_relevant_links(url)
    result = f"## Landing Page:\n\n{contents}\n## Relevant Links:\n"
    for link in relevant_links["links"]:
        result += f"\n\n### Link: {link['type']}\n"
        result += fetch_website_contents(link["url"])
    return result


# System Prompt: This is always the same so it is a simple variable.
# brochure_system_prompt = """
# You are an assistant that analyzes the contents of several relevant pages from a company website
# and creates a short brochure about the company for prospective customers, investors and recruits.
# Respond in markdown without code blocks.
# Include details of company culture, customers and careers/jobs if you have the information.
# """
# Or uncomment the lines below for a more humorous brochure - this demonstrates how easy it is to incorporate 'tone':

brochure_system_prompt = """
You are an assistant that analyzes the contents of several relevant pages from a company website
and creates a short, humorous, entertaining, witty brochure about the company for prospective customers, investors and recruits.
Respond in markdown without code blocks.
Include details of company culture, customers and careers/jobs if you have the information.
"""


# User prompt
def get_brochure_user_prompt(company_name, url):
    user_prompt = f"""
You are looking at a company called: {company_name}
Here are the contents of its landing page and other relevant pages;
use this information to build a short brochure of the company in markdown without code blocks.\n\n
"""
    user_prompt += fetch_page_and_all_relevant_links(url)
    user_prompt = user_prompt[
        :5_000
    ]  # Truncate if more than 5,000 characters (keep down costs if necesary)
    return user_prompt


def create_brochure(company_name, url):
    response = openai.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": brochure_system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(company_name, url)},
        ],
    )
    result = response.choices[0].message.content
    return result


print(create_brochure("HuggingFace", "https://huggingface.co"))
