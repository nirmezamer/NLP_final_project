import google.generativeai as genai
import json
import time
from tqdm import tqdm


genai.configure(api_key="AIzaSyA_a9NStJj6XoMDaGXlbz-v35xCQzTlDqA")
model = genai.GenerativeModel('gemini-1.5-flash')


def create_AI_paper(title, content):
    prompt = f"""Please generate a short newspaper article based on the provided title and content.
The article should be between 100-150 words, brief, informative, and written in a neutral tone. 
It should adhere to a professional newspaper style, ensuring clarity and conciseness, and include specific details like dates, names, and places.
Incorporate quotes and sources where appropriate, and conclude with a short statement highlighting the topic's significance. 
The article must be original, written in your own words, and should closely align with the provided title and content.

The Title is: {title}

The Content is: {content}

Please recreate the newspaper article accordingly and provide me only the article content.
"""

    try:
        answer = call_prompt_with_retry(prompt)
        return answer
    except Exception as e:
        print(f"Error generating content: {e}, title: {title}")
        return ""
    

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

with open('articles_edited.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

ai_data = {}

for key in tqdm(data.keys()):
    title = key
    content = data[key]
    AI_article = create_AI_paper(title, content)
    if AI_article == "":
        continue
    ai_data[key] = AI_article
    with open('AI_articles.json', 'w', encoding='utf-8') as f:
        json.dump(ai_data, f, ensure_ascii=False, indent=4)


