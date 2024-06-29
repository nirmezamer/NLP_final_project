
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
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
import gc
import os

nltk.download('punkt')
# data_jasons = {"reddit": "example_reddit_data_set.json", "wikipedia": "wikipedia_data_set.json", "news": "wikipedia_data_set.json"}
# data_jasons = {"reddit": "reddit/example_reddit_data_set.json"}
data_jasons = {"wikipedia": "modified_file.json"}
dataset = read_data(data_jasons)

# Separate the data and label from the dataset
data = [item[0] for item in dataset]
label = [item[1] for item in dataset]

# Create a dictionary with the desired column names
data_dict = {"data": data, "label": label}

# Convert the dictionary to a pandas DataFrame
df = pd.DataFrame(data_dict)



tqdm.pandas(desc="Tokenizing Text")
df['tokens'] = df['data'].progress_apply(lambda x: word_tokenize(str(x)))
df['characters'] = df['data'].progress_apply(lambda x: len(str(x)))
df['words'] = df['tokens'].progress_apply(lambda tokens: len(tokens))
df['unique_words'] = df['tokens'].progress_apply(lambda x: len(set(x)))
df['sentences'] = df['data'].progress_apply(lambda x: len(sent_tokenize(str(x))))
# Display the first few rows of the DataFrame


plt.figure(figsize=(12, 6))
plt.hist([df[df['label'] == 0]['unique_words'], df[df['label'] == 1]['unique_words']], bins=100, alpha=0.5, label=['Human', 'AI'])
plt.title('number of unique words Distribution by Class')
plt.xlabel('n_unique_words')
plt.ylabel('Frequency')
plt.xlim(right=900)
plt.legend()
plt.show()

plt.figure(figsize=(12, 6))
plt.hist([df[df['label'] == 0]['characters'], df[df['label'] == 1]['characters']], bins=300, alpha=0.5, label=['Human', 'AI'])
plt.title('number of characters Distribution by Class')
plt.xlabel('n_characters')
plt.ylabel('Frequency')
plt.xlim(right=10000)
plt.legend()
plt.show()

plt.figure(figsize=(12, 6))
plt.hist([df[df['label'] == 0]['words'], df[df['label'] == 1]['words']], bins=300, alpha=0.5, label=['Human', 'AI'])
plt.title('Number of Words Distribution by Class')
plt.xlabel('n_words')
plt.ylabel('Frequency')
plt.xlim(right=2000)
plt.legend()
plt.show()


plt.figure(figsize=(12, 6))
plt.hist([df[df['label'] == 0]['sentences'], df[df['label'] == 1]['sentences']], bins=300, alpha=0.5, label=['Human', 'AI'])
plt.title('Number of Sentences Distribution by Class')
plt.xlabel('n_sentences')
plt.ylabel('Frequency')
plt.xlim(right=80)
plt.legend()
plt.show()

gc.collect()
# font_path = 'C:/Windows/Fonts/Arial.ttf'
# if not os.path.exists(font_path):
#     raise FileNotFoundError(f"Font file not found at {font_path}")
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(df[df['label'] == 0]['data']))
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.title('Word Cloud for Human')
plt.axis('off')
plt.show()


wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(df[df['label'] == 1]['data']))
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.title('Word Cloud for AI')
plt.axis('off')
plt.show()

n_grams = [1,2,3]
for n in n_grams:
    df[f'{n}_grams'] = df['tokens'].progress_apply(lambda x: list(ngrams(x, n)))
label_to_text = {0: 'Human', 1: 'AI'}
for label in df['label'].unique():
    subset_df = df[df['label'] == label]
    for n in n_grams:
        ngram_freq = [item for sublist in subset_df[f'{n}_grams'] for item in sublist]
        ngram_freq_dist = pd.Series(ngram_freq).value_counts()

       
        plt.figure(figsize=(12, 6))
        ngram_freq_dist.head(60).plot(kind='bar', color='skyblue')
        plt.title(f'Top 60 Most Frequent {n}-grams for Class: {label_to_text[label]}')
        plt.xlabel('N-gram')
        plt.ylabel('Frequency')
        plt.show()

sia = SentimentIntensityAnalyzer()
tqdm.pandas(desc="Calculating Sentiment Scores")
df['sentiment_score'] = df['data'].progress_apply(lambda x: sia.polarity_scores(str(x))['compound'])

plt.figure(figsize=(10, 6))
plt.hist([df[df['generated'] == 0]['sentiment_score'], df[df['generated'] == 1]['sentiment_score']], bins=100, alpha=0.5, label=['Human', 'AI'])
plt.title('sentiment_score Distribution by Class')
plt.xlabel('sentiment_score')
plt.ylabel('Frequency')
# plt.xlim(right=1,left=0)
plt.ylim(top=6000)
plt.legend()
plt.show()