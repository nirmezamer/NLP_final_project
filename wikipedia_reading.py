import wikipediaapi
import google.generativeai as genai
import requests


genai.configure(api_key="AIzaSyANbFX_VEG9NW3LHr-3xEAyTF5r0F5tNw0")

model = genai.GenerativeModel('gemini-1.5-flash')

msg = """Please generate a Wikipedia-style summary of a random topic. The summary should be informative, neutral in tone, and written in an encyclopedic style typical of Wikipedia articles. Ensure the summary includes key aspects such as the topic's significance, relevant history, notable features, and important figures. The information should sound credible and include specific details like dates, names, and places. The summary should be a single, well-structured paragraph."""


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
    print(prompt.text)
    return prompt


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
    return summary

# call_prompt(msg)

for i in range(10):
    print(get_random_wikipedia_article(), "\n", "-"*50, "\n")
