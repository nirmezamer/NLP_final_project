import json
import praw
import random
import os
import shutil

# Replace these with your own credentials
CLIENT_ID = '39ZflIZLYQso2iFg9GqW2g'
CLIENT_SECRET = 'OnT4P7VFwU4gP6-Zz4Ke8y42FkcunQ'
USER_AGENT = 'your_user_agent'

def get_subreddits_list():
    subreddits = [
    # General Interest
    "AskReddit", "IAmA", 
    
    # Technology
    "technology", "gadgets", 
    
    # Science
    "science", "space", 
    
    # Entertainment
    "movies", "television", 
    
    # Hobbies and Interests
    "cooking", "fitness", 
    
    # Gaming
    "gaming", "pcgaming", 
    
    # Art and Creativity
    "Art", "Design", 
    
    # Humor
    "funny", "Memes", 
    
    # Lifestyle
    "LifeProTips", "GetMotivated", 
    
    # News and Politics
    "news", "worldnews", 
    
    # Miscellaneous
    "cats", "dogs", 
    ]

    return subreddits

def gen_single_reddit_json(subreddit_name, file_name):
    reddit = praw.Reddit(client_id=CLIENT_ID,
                         client_secret=CLIENT_SECRET,
                         user_agent=USER_AGENT)

    subreddit = reddit.subreddit(subreddit_name)
    
    num_posts = 20
    posts = list(subreddit.hot(limit=num_posts)) 
    
    posts_dict = {}
    for post in posts:
        posts_dict[post.title] = {
            "title": post.title,
            "score": post.score,
            "url": post.url,
            "content": post.selftext,
            "num_comments": post.num_comments,
            "comments": [comment.body for comment in post.comments.list() if type(comment) == praw.models.Comment]
        }
    with open(file_name, "w") as file:
        json.dump(posts_dict, file, indent=4)

def gen_many_humanities_reddit_json():
    
    subreddits = get_subreddits_list()
    new_dir_path = "./reddit_humanities_data_new"
    if not os.path.exists(new_dir_path):
        os.makedirs(new_dir_path)
    
    for subreddit in subreddits:
        gen_single_reddit_json(subreddit, new_dir_path + "/" + subreddit + ".json")
        
    dir_path = "./reddit_humanities_data"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    overide = ""
    while overide != "y" and overide != "n":
        overide = input("Do you want to override the existing data? (y/n): ")
    
    if overide == "y":
        ## remove the dir in dir_path and replace with new_dir_path in windows
        shutil.rmtree(dir_path)
        os.rename(new_dir_path, dir_path)
    
    print("Data collection complete.")
    return
    

# Example usage
if __name__ == "__main__":
    
    # gen_single_reddit_json('python', "reddit_postd.json")  # Replace 'python' with any subreddit name
    gen_many_humanities_reddit_json()