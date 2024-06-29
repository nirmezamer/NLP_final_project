import newspaper
import logging
import re
import json
import google.generativeai as genai

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

def create_AI_paper(title):
    prompt = """Please generate a short newspaper content for a given title. 
The newspaper content should be brief, informative, neutral in tone, and written in a newspaper style. 
Ensure the newspaper content includes quotes and sources, proffetional style and a short conclusion such as the topic's significance. 
The information should sound clarity and conciseness and include specific details like dates, names, and places. 
Write the newspaper content in your own words, avoiding direct copying from existing newspapers. 
The newspaper content should be concise, typically around 3-5 sentences, and should closely resemble the style and length of actual Wikipedia summaries. 
The title will be provided, and the generated summary should align closely with the title's topic.

The Title is:
"""
    prompt += title
    try:
        answer = call_prompt_with_retry(prompt)
        return answer
    except Exception as e:
        return ""

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