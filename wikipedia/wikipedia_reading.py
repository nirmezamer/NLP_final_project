import wikipediaapi
import google.generativeai as genai
import requests
import json
import numpy as np
from tqdm import tqdm
import time

GEN_HUMAN_SUMMARIES = False
GEN_LLM_SUMMARIES   = True

NUM_HUMAN_SUMMARIES = 2000
NUM_LLM_SUMMARIES   = 2000

genai.configure(api_key="AIzaSyCndWWxDbmMg99QowJPxeZDfB8LHWm1y7Y")

model = genai.GenerativeModel('gemini-1.5-flash')

msg = """Please generate a Wikipedia-style summary for the given title. The summary should be brief, informative, neutral in tone, and written in an encyclopedic style typical of Wikipedia articles. Ensure the summary includes key aspects such as the topic's significance, relevant history, notable features, and important figures. The information should sound credible and include specific details like dates, names, and places. Write the summary in your own words, avoiding direct copying from existing Wikipedia articles. The summary should be concise, typically around 3-5 sentences, and should closely resemble the style and length of actual Wikipedia summaries. The title will be provided, and the generated summary should align closely with the title's topic.

Title: """


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

def call_prompt_with_retry(msg, retries=5, backoff_factor=1):
    for i in range(retries):
        try:
            answer = model.generate_content(msg)
            if answer != "":
                return answer.text
        except Exception as e:
            if "429" in str(e):
                wait_time = backoff_factor * (2 ** i)
                print(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                return ""
    return ""


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

def get_random_wikipedia_title():
    # Wikipedia API endpoint for random articles
    url = "https://en.wikipedia.org/api/rest_v1/page/random/summary"
    params = {
        "action": "query",
        "format": "json",
        "list": "random",
        "rnlimit": 1
    }
    title = ""
    while title == "":
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            title = data['title']
        except requests.exceptions.RequestException as e:
            print(f"Error fetching Wikipedia article: {e}")
            return ""
    return title

if GEN_HUMAN_SUMMARIES:
    human_data = {}
    for i in tqdm(range(NUM_HUMAN_SUMMARIES)):
        title, summary = get_random_wikipedia_article()
        human_data[title] = summary

    with open("human_wikipedia_summaries.json", "w") as file:
        json.dump(human_data, file)

if GEN_LLM_SUMMARIES:
    LLM_summaries = {}
    wikipedia_titles = []
    with open("wikipedia_titles.json", "r") as file:
        wikipedia_titles = json.load(file)
    # for i in tqdm(range(NUM_LLM_SUMMARIES)):
    #     title = get_random_wikipedia_title()
    #     if title == "":
    #         continue
    #     wikipedia_titles.append(title)
    # with open("wikipedia_titles.json", "w") as file:
    #     json.dump(wikipedia_titles, file, indent=4)


    checkpoint_interval = 10  # Define how often to write checkpoints (every 10 iterations)

    with open("ai_wikipedia_summaries.json", "w") as file:
        file.write("{\n")
        
        for i in tqdm(range(len(wikipedia_titles))):
            answer = call_prompt_with_retry(msg + '"' + wikipedia_titles[i] + '"')
            if answer == "":
                continue
            LLM_summaries[wikipedia_titles[i]] = answer
            
            # Write the current summary to the JSON file as an intermediate checkpoint
            json.dump({wikipedia_titles[i]: answer}, file)
            if i < (len(wikipedia_titles) - 1):
                file.write(",\n")  # Add a comma and newline for all but the last entry

            # Periodically write intermediate results to a separate file as a checkpoint
            if i % checkpoint_interval == 0:
                with open("ai_wikipedia_summaries_checkpoint.json", "w") as checkpoint_file:
                    json.dump(LLM_summaries, checkpoint_file, indent=4)
        
            file.write("\n}\n")  # Close the JSON object properly

        # Write the final dictionary to the checkpoint file once more to ensure it's up-to-date
        with open("ai_wikipedia_summaries_checkpoint.json", "w") as checkpoint_file:
            json.dump(LLM_summaries, checkpoint_file, indent=4)
                
        