import requests

# Replace 'YOUR_API_KEY' with your actual API key
api_key = '8eXt8AOv6GKrkzV6sK6ipDaQxgWji44g'
type_list = ['arts', 'automobiles', 'business', 'fashion', 'food', 'health', 'home', 'insider', 'magazine', 'movies', 'nyregion', 'obituaries', 'opinion', 'politics', 'realestate', 'science', 'sports', 'sundayreview', 'technology', 'theater', 't-magazine', 'travel', 'upshot', 'us', 'world']
urls = [f'https://api.nytimes.com/svc/topstories/v2/{i}.json?api-key={api_key}' for i in type_list]
data_json = {}
for url in urls:
    response = requests.get(url)
    data = response.json()
    for article in data['results']:
        article_url = article['url']
        api_url = f'https://api.nytimes.com/svc/search/v2/articlesearch.json?api-key={api_key}&fq=web_url:("{article_url}")'
        article_response = requests.get(api_url)
        article_data = article_response.json()  # Assuming the article data is in JSON format

        # Extract full article content
        full_article = article_data.get('content', '')
        if full_article:
            print(f"Headline: {article['title']}")
            print(f"Full Article: {full_article}")
            print('---')
        else:
            print(f"Headline: {article['title']}")
            print("Full article not available.")
            print('---')


# # Print the headlines and summaries of the latest articles
# for article in data['results']:
#     headline = article['title']
#     summary = article['abstract']
#     print(headline)
#     print(summary)
#     print('---')