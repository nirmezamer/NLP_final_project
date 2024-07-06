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

