import newspaper
import json
import asyncio
from tqdm import tqdm
import time
from async_timeout import timeout
import aiohttp
import random


# List of sections for each news website
news_sites = {
    'bbc': [
        'http://www.bbc.com/news',
        'http://www.bbc.com/news/world',
        'http://www.bbc.com/news/business',
        'http://www.bbc.com/news/technology',
        'http://www.bbc.com/news/science_and_environment',
        'http://www.bbc.com/news/entertainment_and_arts',
        'http://www.bbc.com/news/health',
        'http://www.bbc.com/news/education',
        'http://www.bbc.com/news/magazine',
        'http://www.bbc.com/news/in_pictures',
    ],
    'fox': [
        'http://www.foxnews.com',
        'http://www.foxnews.com/world',
        'http://www.foxnews.com/politics',
        'http://www.foxnews.com/tech',
        'http://www.foxnews.com/science',
        'http://www.foxnews.com/entertainment',
        'http://www.foxnews.com/health',
        'http://www.foxnews.com/lifestyle',
        'http://www.foxnews.com/opinion',
    ],
    'nyt': [
        'https://www.nytimes.com',
        'https://www.nytimes.com/section/world',
        'https://www.nytimes.com/section/business',
        'https://www.nytimes.com/section/technology',
        'https://www.nytimes.com/section/science',
        'https://www.nytimes.com/section/arts',
        'https://www.nytimes.com/section/health',
        'https://www.nytimes.com/section/education',
        'https://www.nytimes.com/section/opinion',
    ],
    'cnn': [
        'http://www.cnn.com',
        'http://www.cnn.com/world',
        'http://www.cnn.com/business',
        'http://www.cnn.com/tech',
        'http://www.cnn.com/science',
        'http://www.cnn.com/entertainment',
        'http://www.cnn.com/health',
        'http://www.cnn.com/travel',
        'http://www.cnn.com/opinions',
    ],
    'guardian': [
        'https://www.theguardian.com/international',
        'https://www.theguardian.com/world',
        'https://www.theguardian.com/business',
        'https://www.theguardian.com/technology',
        'https://www.theguardian.com/environment',
        'https://www.theguardian.com/culture',
        'https://www.theguardian.com/society',
        'https://www.theguardian.com/lifeandstyle',
        'https://www.theguardian.com/commentisfree',
    ],
    'reuters': [
        'https://www.reuters.com',
        'https://www.reuters.com/news/world',
        'https://www.reuters.com/news/business',
        'https://www.reuters.com/news/technology',
        'https://www.reuters.com/news/science',
        'https://www.reuters.com/news/entertainment',
        'https://www.reuters.com/news/health',
        'https://www.reuters.com/news/lifestyle',
        'https://www.reuters.com/finance',
    ],
    'washington_post': [
        'https://www.washingtonpost.com',
        'https://www.washingtonpost.com/world',
        'https://www.washingtonpost.com/business',
        'https://www.washingtonpost.com/technology',
        'https://www.washingtonpost.com/health',
        'https://www.washingtonpost.com/entertainment',
        'https://www.washingtonpost.com/lifestyle',
        'https://www.washingtonpost.com/opinions',
        'https://www.washingtonpost.com/local',
    ],
    'bbc_sport': [
        'http://www.bbc.com/sport',
        'http://www.bbc.com/sport/football',
        'http://www.bbc.com/sport/formula1',
        'http://www.bbc.com/sport/tennis',
        'http://www.bbc.com/sport/golf',
        'http://www.bbc.com/sport/cricket',
        'http://www.bbc.com/sport/rugby-union',
        'http://www.bbc.com/sport/cycling',
        'http://www.bbc.com/sport/motorsport',
    ],
    'business_insider': [
        'https://www.businessinsider.com',
        'https://www.businessinsider.com/sai',
        'https://www.businessinsider.com/clusterstock',
        'https://www.businessinsider.com/insider',
        'https://www.businessinsider.com/tech',
        'https://www.businessinsider.com/finance',
        'https://www.businessinsider.com/politics',
        'https://www.businessinsider.com/strategy',
        'https://www.businessinsider.com/life',
    ],
    'usatoday': [
        'https://www.usatoday.com',
        'https://www.usatoday.com/news',
        'https://www.usatoday.com/money',
        'https://www.usatoday.com/tech',
        'https://www.usatoday.com/sports',
        'https://www.usatoday.com/life',
        'https://www.usatoday.com/travel',
        'https://www.usatoday.com/opinion',
        'https://www.usatoday.com/picture-gallery',
    ],
    # New additions
    'ap': [
        'https://apnews.com',
        'https://apnews.com/hub/world-news',
        'https://apnews.com/hub/us-news',
        'https://apnews.com/hub/politics',
        'https://apnews.com/hub/business',
        'https://apnews.com/hub/technology',
        'https://apnews.com/hub/health',
        'https://apnews.com/hub/science',
        'https://apnews.com/hub/entertainment',
    ],
    'npr': [
        'https://www.npr.org',
        'https://www.npr.org/sections/news',
        'https://www.npr.org/sections/politics',
        'https://www.npr.org/sections/business',
        'https://www.npr.org/sections/technology',
        'https://www.npr.org/sections/health',
        'https://www.npr.org/sections/science',
        'https://www.npr.org/sections/arts',
        'https://www.npr.org/sections/education',
    ],
    'bloomberg': [
        'https://www.bloomberg.com',
        'https://www.bloomberg.com/markets',
        'https://www.bloomberg.com/technology',
        'https://www.bloomberg.com/politics',
        'https://www.bloomberg.com/businessweek',
        'https://www.bloomberg.com/pursuits',
        'https://www.bloomberg.com/green',
        'https://www.bloomberg.com/wealth',
        'https://www.bloomberg.com/citylab',
    ],
    'abc_news': [
        'https://abcnews.go.com',
        'https://abcnews.go.com/US',
        'https://abcnews.go.com/International',
        'https://abcnews.go.com/Politics',
        'https://abcnews.go.com/Business',
        'https://abcnews.go.com/Technology',
        'https://abcnews.go.com/Health',
        'https://abcnews.go.com/Entertainment',
        'https://abcnews.go.com/Sports',
    ],
    'huffpost': [
        'https://www.huffpost.com',
        'https://www.huffpost.com/news',
        'https://www.huffpost.com/entertainment',
        'https://www.huffpost.com/life',
        'https://www.huffpost.com/section/politics',
        'https://www.huffpost.com/voices',
        'https://www.huffpost.com/section/world-news',
        'https://www.huffpost.com/section/business',
        'https://www.huffpost.com/section/technology',
    ]
}



articles = []
seen_urls = set()
max_articles_per_site = 10  # Adjust this to limit articles per site (optional)


async def scrape_articles_async(url, session, progress_bar):
    try:
        article = newspaper.Article(url, fetch_images=False)  # Avoid image downloads
        async with session.get(url) as response:
            if response.status == 200:
                article.download_html(response.text)
                article.parse()
                if article.url not in seen_urls and (not max_articles_per_site or len(articles) < max_articles_per_site):
                    seen_urls.add(article.url)
                    articles.append({
                        'title': article.title,
                        'text': article.text,
                        'authors': article.authors,
                        'publish_date': article.publish_date,
                        'url': article.url
                    })
                    progress_bar.update(1)
            else:
                print(f"Error getting article: {url} - Status code: {response.status}")
    except (aiohttp.ClientError, newspaper.newspaper3k.ArticleException) as e:
        print(f"Error processing article: {url} - {e}")
    await asyncio.sleep(random.randint(1, 2))  # Introduce random delay between requests


async def scrape_all_articles(news_sites, progress_bar):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for site, urls in news_sites.items():
            for url in urls:
                tasks.append(scrape_articles_async(url, session, progress_bar))
        await asyncio.gather(*tasks)


async def main():
    total_articles_to_scrape = sum(len(urls) for urls in news_sites.values())
    with tqdm(total=total_articles_to_scrape, desc="Scraping Articles") as progress_bar:
        await scrape_all_articles(news_sites, progress_bar)


if __name__ == "__main__":
    asyncio.run(main())

# Save the articles to a JSON file (optional)
output_file = 'articles_2.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=4)

print(f"Scraped a total of {len(articles)} articles. Saved to {output_file}")  # Modify if not saving