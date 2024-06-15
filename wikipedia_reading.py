import wikipediaapi
import google.generativeai as genai
import requests
import json
import numpy as np
from tqdm import tqdm

genai.configure(api_key="AIzaSyANbFX_VEG9NW3LHr-3xEAyTF5r0F5tNw0")

model = genai.GenerativeModel('gemini-1.5-flash')

msg = """Please generate a Wikipedia-style summary of a random topic. The summary should be informative, neutral in tone, and written in an encyclopedic style typical of Wikipedia articles. Ensure the summary includes key aspects such as the topic's significance, relevant history, notable features, and important figures. The information should sound credible and include specific details like dates, names, and places. The summary should be a single, well-structured paragraph. after all that generate a title to the summary ass well that will be fit to wikipedia-style topic. i want the title to be at the start and will be following with a """


def read_wikipedia_page(page_title):
    wiki_wiki = wikipediaapi.Wikipedia(
        language='en',
        extract_format=wikipediaapi.ExtractFormat.WIKI,
        user_agent='My Python Application'
    )
    page = wiki_wiki.page(page_title)
    if page.exists():
        if page.summary == "":
            return "Page exists but has no summary"
        return page.summary
    else:
        return "Page does not exist"

def call_prompt(msg):
    prompt = model.generate_content(msg)
    
    return prompt.text


def get_random_wikipedia_article():
    wiki_wiki = wikipediaapi.Wikipedia(language='en',
        extract_format=wikipediaapi.ExtractFormat.WIKI,
        user_agent='My Python Application')

    # Wikipedia API endpoint for random articles
    url = "https://en.wikipedia.org/api/rest_v1/page/random/summary"
    params = {
        "action": "query",
        "format": "json",
        "list": "random",
        "rnlimit": 1
    }
    summary = ""
    while summary == "":
    
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            random_article_title = data['title']
            page = wiki_wiki.page(random_article_title)
            summary = page.summary


        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching Wikipedia article: {e}")
    return random_article_title, summary

# call_prompt(msg)
num_human_summaries = 10
num_LLM_summaries = 10
human_data = {}
for i in tqdm(range(num_human_summaries)):
    title, summary = get_random_wikipedia_article()
    human_data[title] = summary

with open("humen_wikipedia_summaries.json", "w") as file:
    json.dump(human_data, file)


LLM_data = {}
for i in tqdm(range(num_LLM_summaries)):
    prompt = call_prompt(msg)
    LLM_data[i] = prompt
with open("LLM_wikipedia_summaries.json", "w") as file:
    json.dump(LLM_data, file)