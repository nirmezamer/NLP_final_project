import json
import praw
import random
import os
import shutil
import google.generativeai as genai
from tqdm import tqdm

genai.configure(api_key="AIzaSyA_a9NStJj6XoMDaGXlbz-v35xCQzTlDqA")
model = genai.GenerativeModel('gemini-1.5-flash')

def call_prompt(prompt):
    answer = call_prompt_with_retry(prompt)
    return answer

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


# Replace these with your own credentials
CLIENT_ID = '39ZflIZLYQso2iFg9GqW2g'
CLIENT_SECRET = 'OnT4P7VFwU4gP6-Zz4Ke8y42FkcunQ'
USER_AGENT = 'your_user_agent'

reddit = praw.Reddit(client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        user_agent=USER_AGENT)

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

def gen_single_reddit_json(subreddit, file_name, num_posts=5):

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

def generate_many_humanities_reddit_json():
    
    subreddits = get_subreddits_list()
    subreddits = reddit.subreddits.popular(limit=2000)
    new_dir_path = "./reddit/reddit_humanities_data_new"
    if not os.path.exists(new_dir_path):
        os.makedirs(new_dir_path)
    
    for i, subreddit in tqdm(enumerate(subreddits)):
        subreddit_name = subreddit.display_name
        json_file_name = new_dir_path + "/" + subreddit_name + ".json"
        if os.path.exists(json_file_name):
            continue
        gen_single_reddit_json(subreddit, json_file_name)
        
    dir_path = "./reddit/reddit_humanities_data"
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
    
def get_humanities_reddit_data():
    # data[<subreddit_name>]
    #     [<post_title>]
    #     ["title"|"score"|"url"|"content"|"num_comments"|"comments"]
    
    dir_path = "./reddit/reddit_humanities_data"
    
    data = {}
    for file in os.listdir(dir_path):
        with open(dir_path + "/" + file, "r") as f:
            data[file.split(".")[0]] = json.load(f)
    
    return data

def generate_AI_comment(title, content, human_comments):
    comments = "\n".join(human_comments)
    prompt = f"""You will be provided with a Reddit post and a subset of its comments. Your task is to generate a new comment that fits naturally into the conversation. The generated comment should be coherent, contextually appropriate, and human-like. The goal is to create a comment that would make sense if it appeared in the original thread.

Instructions:
Read the provided Reddit post carefully.
Review the provided comments to understand the context and tone of the discussion.
Generate a new comment that could naturally follow the provided comments and align with the ongoing discussion.
Ensure the comment is relevant to the post and the preceding comments.
Your comment should:

Be well-written and free of grammatical errors.
Maintain a tone consistent with the other comments.
Provide a meaningful contribution to the conversation.
Output only the comment text. Do not include any introductions, explanations, or closing statements.

Reddit Post:
Title: {title}
Body: {content}

Comments:
{comments}
Your Generated Comment:
    """
    try:
        answer = call_prompt(prompt)
        return answer.text
    except Exception as e:
        return ""

def generate_reddit_data_set():
    # data_set[<post_title>]["title"|"content"|"human_comment"|"AI_comment"]
    data_set = {}
    raw_data = get_humanities_reddit_data()
    
    for i, subreddit in tqdm(enumerate(raw_data.keys())):
        subreddit_data = raw_data[subreddit]
        for post in enumerate(subreddit_data.keys()):
            if subreddit_data[post]["num_comments"] < 10:
                continue
            AI_comment = generate_AI_comment(subreddit_data[post]["title"], \
                                             subreddit_data[post]["content"], \
                                             subreddit_data[post]["comments"][1:5])
            if AI_comment == "":
                # Save the data set to a json file
                with open("reddit/reddit_data_set.json", "w") as file:
                    json.dump(data_set, file, indent=4)
                continue
            data_set[post] = {
                "title": subreddit_data[post]["title"],
                "content": subreddit_data[post]["content"],
                "human_comment": subreddit_data[post]["comments"][0],
                "AI_comment": AI_comment
            }
            
    # Save the data set to a json file
    with open("reddit/reddit_data_set.json", "w") as file:
        json.dump(data_set, file, indent=4)
        
    return data_set
        
def clean_up_jsons():
    dir_path = "./reddit/reddit_humanities_data_new"
    for file in os.listdir(dir_path):
        with open(dir_path + "/" + file, "r") as f:
            data = json.load(f)
        for post in data.keys():
            if len(data[post]["comments"]) > 10:
                data[post]["comments"] = data[post]["comments"][:10]
        with open(dir_path + "/" + file, "w") as f:
            json.dump(data, f, indent=4)
    return

# Example usage
if __name__ == "__main__":
    
    data = generate_reddit_data_set()
    print(len(data))

    # generate_many_humanities_reddit_json()
    # clean_up_jsons()