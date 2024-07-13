
from read_datasets import read_data
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import word_tokenize , sent_tokenize
from nltk.corpus import stopwords
from wordcloud import WordCloud
from tqdm import tqdm
from nltk import ngrams
from string import punctuation
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
# from textblob import TextBlob
import gc
# import os

nltk.download('punkt')
nltk.download('vader_lexicon')
# data_jasons = {"reddit": "example_reddit_data_set.json", "wikipedia": "wikipedia_data_set.json", "news": "wikipedia_data_set.json"}
# data_jasons = {"reddit": "reddit/example_reddit_data_set.json"}
data_jasons = {"newspaper": "newspaper/newspapers_data.json","wikipedia": "wikipedia/wikipedia_summaries.json", "reddit": "reddit/reddit_data_set.json"}


def data_to_pd(dataset):
    # Separate the data and label from the dataset
    data = [item[0] for item in dataset]
    label = [item[1] for item in dataset]

    # Create a dictionary with the desired column names
    data_dict = {"data": data, "label": label}

    # Convert the dictionary to a pandas DataFrame
    df = pd.DataFrame(data_dict)
    return df

plt.figure(figsize=(16, 6))
plt.suptitle('Number of unique words distribution by class')
for i, key in enumerate(list(data_jasons.keys())):
    dataset = {}
    dataset[key] = data_jasons[key]
    dataset = read_data(dataset)


    df = data_to_pd(dataset)


    tqdm.pandas(desc="Tokenizing Text")
    df['tokens'] = df['data'].progress_apply(lambda x: word_tokenize(str(x)))
    df['characters'] = df['data'].progress_apply(lambda x: len(str(x)))
    df['words'] = df['tokens'].progress_apply(lambda tokens: len(tokens))
    df['unique_words'] = df['tokens'].progress_apply(lambda x: len(set(x)))
    df['sentences'] = df['data'].progress_apply(lambda x: len(sent_tokenize(str(x))))
    # Display the first few rows of the DataFrame


    plt.subplot(1, 3, i+1)
    plt.hist([df[df['label'] == 0]['unique_words'], df[df['label'] == 1]['unique_words']], bins=100, alpha=0.5, label=['Human', 'AI'])
    plt.title(f'{key.capitalize()}')
    plt.xlabel('Number of unique words')
    plt.ylabel('Frequency')
    if key == 'newspaper':
        x_lim = 700
        y_lim = 24
    if key == 'reddit':
        x_lim = 100
        y_lim = 600
    if key == 'wikipedia':
        x_lim = 300
        y_lim = 400
    plt.xlim(right=x_lim)
    plt.ylim(top=y_lim)
    plt.xticks(range(0, x_lim+1, int(x_lim/10)))
    plt.yticks(range(0, y_lim+1, int(y_lim/10)))
    plt.legend()
    plt.grid(True)
plt.savefig(f'analysis/unique_words.png')

