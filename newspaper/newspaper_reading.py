import newspaper
import logging
import re
import json
import google.generativeai as genai
import time

# genai configuration
genai.configure(api_key="AIzaSyA_a9NStJj6XoMDaGXlbz-v35xCQzTlDqA")
model = genai.GenerativeModel('gemini-1.5-flash')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def build_paper(url, memoize_articles=False):
    try:
        paper = newspaper.build(url, memoize_articles=memoize_articles)
        logger.info(f"Successfully built paper from {url}")
        return paper
    except Exception as e:
        logger.error(f"Error building paper from {url}: {e}")
        return None

def fetch_articles(paper):
    if paper and paper.size() > 0:
        article_urls = [article.url for article in paper.articles if re.match(r'https?://www\.bbc\.com/news/', article.url)]
        logger.info(f"Found {len(article_urls)} articles")
        return article_urls
    else:
        logger.warning("No articles found")
        return []

def download_article(article):
    try:
        article.download()
        article.parse()
        logger.info("Article downloaded and parsed successfully")
        return article.text, article.title
    except Exception as e:
        logger.error(f"Error downloading/parsing article: {e}")
        return "", ""

def save_to_json(articles_dict, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(articles_dict, f, ensure_ascii=False, indent=4)
    logger.info(f"Saved articles to {filename}")

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
        return ""

def create_AI_generated_paper(papers):
    # papers is a dictionary with title and content
    # papers['title'] = 'content'
    generated_papers = {}
    for title, content in papers.items():
        generated_paper = create_AI_paper(title, content)
        if generated_paper == "":
            logger.error(f"Error generating content for {title}")
        else:
            generated_papers[title] = generated_paper
    
    # Save the generated papers to a JSON file
    file_name = "AI_generated_papers.json"
    with open(file_name, "w") as file:
        json.dump(generated_papers, file, indent=4)
        
    return generated_papers
    
def main():
    # Example website to try
    website = 'http://bbc.com'

    logger.info(f"Processing website: {website}")
    paper = build_paper(website)

    if paper:
        article_urls = fetch_articles(paper)
        articles_data = {}

        if article_urls:
            logger.info(f"Saving text of {len(article_urls)} articles to JSON file...")
            for url in article_urls:
                article = newspaper.Article(url)
                text, title = download_article(article)
                if text and title:
                    articles_data[title] = text.strip()

        save_to_json(articles_data, 'bbc_articles.json')

if __name__ == "_main_":
    main()