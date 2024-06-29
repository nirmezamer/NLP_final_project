import numpy as np
import pandas as pd
from read_datasets import read_data
from analyze_dataset import data_to_pd
import json
from better_profanity import profanity
import re

def contains_explicit(text):
    return profanity.contains_profanity(text)

def clear_data(dataset_path, save_path):
    data = read_data(dataset_path)
    dataset = data_to_pd(data)
    dataset['data'] = dataset['data'].str.replace('^>', '', regex=True)
    dataset = dataset[~dataset['data'].str.contains("I am a bot")]
    # Filter out rows containing explicit content
    filtered_data = dataset[dataset['Data'].apply(contains_explicit)]

    # Save the rows with explicit content to a separate CSV file
    filtered_data.to_csv('explicit_content.csv', index=False)

    # Remove the rows with explicit content from the original DataFrame
    dataset = dataset.drop(filtered_data.index)
    dataset_json = {}
    for i in range(len(dataset)):
        dataset_json[dataset[i]['data']] = {data: dataset[i]['data'], "ai-generated": dataset[i]['label']}
    with open(save_path, 'w') as json_file:
        json.dump(dataset_json, json_file)


def clean_text(text):
    text = re.sub(r'\b(?:https?://|www\.)\S+\b', '', text)
    text = re.sub(r'[^\w\s$.,!?"\']', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'^>', '', text)
    return text, contains_explicit(text)