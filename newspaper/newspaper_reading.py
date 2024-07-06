import newspaper
import logging
import re
import json
import google.generativeai as genai
import time
import random
from tqdm import tqdm


# new york times api key: 8eXt8AOv6GKrkzV6sK6ipDaQxgWji44g

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

def main():
    with open('newspaper/news_sites.json', 'r', encoding='utf-8') as f:
        news_sites = json.load(f)

    articles_data = {}

    # Randomize the order of the websites
    websites = []
    for site, urls in news_sites.items():
        websites.extend(urls)
    random.shuffle(websites)
    failed_urls = []
    for website in websites:
        logger.info(f"Processing website: {website}")
        paper = build_paper(website)

        if paper:
            article_urls = fetch_articles(paper)

            if article_urls:
                with tqdm(total=len(article_urls), desc=f"Processing {website}") as pbar:
                    for url in article_urls:
                        article = newspaper.Article(url)
                        text, title = download_article(article)
                        if title not in articles_data.keys():
                            articles_data[title] = []
                        if text and title:
                            text = text.strip()
                            if text not in articles_data[title]:
                                articles_data[title].append(text.strip())
                            save_to_json(articles_data, 'articles_13_53.json')
                        else:
                            failed_urls.append(url)
                            logger.warning(f"Failed to download article: {url}, number of failed urls: {len(failed_urls)}")
                        pbar.update(1)  # Update tqdm progress bar
                    
            else:
                failed_urls.append(website)
                logging.warning(f"No articles found on {website}, number of failed urls: {len(failed_urls)}")

        else:
            failed_urls.append(website)
            logging.warning(f"Failed to build paper for {website}, number of failed urls: {len(failed_urls)}")

    # Save all articles data to JSON file
    save_to_json(failed_urls, 'failed_urls.json')

if __name__ == "__main__":
    main()


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

# def main():
#     # Example website to try
#     website = 'http://bbc.com'

#     logger.info(f"Processing website: {website}")
#     paper = build_paper(website)

#     if paper:
#         article_urls = fetch_articles(paper)
#         articles_data = {}

#         if article_urls:
#             logger.info(f"Saving text of {len(article_urls)} articles to JSON file...")
#             for url in article_urls:
#                 article = newspaper.Article(url)
#                 text, title = download_article(article)
#                 if text and title:
#                     articles_data[title] = text.strip()

#         save_to_json(articles_data, 'bbc_articles.json')

# if __name__ == "_main_":
#     main()