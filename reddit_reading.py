import json
import praw
import random

# Replace these with your own credentials
CLIENT_ID = '39ZflIZLYQso2iFg9GqW2g'
CLIENT_SECRET = 'OnT4P7VFwU4gP6-Zz4Ke8y42FkcunQ'
USER_AGENT = 'your_user_agent'

def get_random_reddit_post(subreddit_name):
    reddit = praw.Reddit(client_id=CLIENT_ID,
                         client_secret=CLIENT_SECRET,
                         user_agent=USER_AGENT)

    subreddit = reddit.subreddit(subreddit_name)
    
    num_posts = 10
    posts = list(subreddit.hot(limit=num_posts)) 
    
    posts_dict = {}
    for post in posts:
        posts_dict[post.title] = {
            "title": post.title,
            "score": post.score,
            "url": post.url,
            "content": post.selftext,
            "num_comments": post.num_comments,
            "comments": [comment.body for comment in post.comments.list()]
        }
    with open("reddit_postd.json", "w") as file:
        json.dump(posts_dict, file) 

    # random_post = random.choice(posts)

    # print(f"Title: {random_post.title}")
    # print(f"Score: {random_post.score}")
    # print(f"URL: {random_post.url}")
    # print(f"Content: {random_post.selftext}")
    # print(f"Number of comments: {random_post.num_comments}")
    # print(f"Comments: {random_post.comments.list()[0].body}")

# Example usage
if __name__ == "__main__":
    get_random_reddit_post('python')  # Replace 'python' with any subreddit name
