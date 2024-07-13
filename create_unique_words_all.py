
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

def create_unique_words_all():
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
    plt.savefig(f'analysis/All_datasets_unique_words.png')

def create_2_grams_all():
    top_n = 30

    plt.figure(figsize=(25, 20))
    plt.suptitle(f'Top {top_n} Most Frequent 2-grams\n {{Dataset}} : {{Class}}', fontsize=30)
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

        n = 2
        df[f'{n}_grams'] = df['tokens'].progress_apply(lambda x: list(ngrams(x, n)))
        label_to_text = {0: 'Human', 1: 'AI'}

        for label in [0, 1]:
            plt.subplot(3, 2, i*2 + label + 1)
            plt.subplots_adjust(hspace=0.6)
            
            subset_df = df[df['label'] == label]
            ngram_freq = [item for sublist in subset_df[f'{n}_grams'] for item in sublist]
            ngram_freq_dist = pd.Series(ngram_freq).value_counts()

            ngram_freq_dist.head(top_n).plot(kind='bar', color='skyblue')
            
            plt.title(f'{key.capitalize()} : {label_to_text[label]}', fontsize=20)
            plt.xlabel('N-gram', fontsize=15)
            plt.ylabel('Frequency', fontsize=15)
    plt.savefig(f'analysis/All_2_grams.png')
    
def create_wordcloud_all():
    plt.figure(figsize=(25, 20))
    plt.suptitle(f'Word Clouds for all datasets\n {{Dataset}} : {{Class}}', fontsize=30)
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

        gc.collect()
        # font_path = 'C:/Windows/Fonts/Arial.ttf'
        # if not os.path.exists(font_path):
        #     raise FileNotFoundError(f"Font file not found at {font_path}")
        
        label_to_text = {0: 'Human', 1: 'AI'}
        for label in [0, 1]:
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(df[df['label'] == label]['data']))
            plt.subplot(3, 2, i*2 + label + 1)
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.title(f'{key.capitalize()} : {label_to_text[label]}', fontsize=30)
            plt.axis('off')
    
    plt.savefig(f'analysis/All_word_clouds.png')




if __name__ == '__main__':
    # create_unique_words_all()
    # create_2_grams_all()
    create_wordcloud_all()