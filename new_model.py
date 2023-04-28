from urllib.request import urlopen
import json
from langdetect import detect, LangDetectException
import pandas as pd
import csv
import nltk
from nltk import FreqDist
from nltk.util import ngrams
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')

function_words = json.loads(urlopen(
    "https://raw.githubusercontent.com/bachdumpling/genz-dictionary-model/main/function_words.json").read())


def preprocess(text):
    tokens = nltk.word_tokenize(text.lower())
    stopwords_list = set(stopwords.words('english'))
    return [token for token in tokens if token not in stopwords_list and token not in function_words]


def get_popular_words(comments, top_n=10, threshold_1=0.8, threshold_2=20):
    all_words = []
    all_bigrams = []

    for comment in comments:
        tokens = preprocess(comment)
        all_words.extend(tokens)
        all_bigrams.extend(ngrams(tokens, 2))

    total_comments = len(comments)
    unigram_freq = FreqDist(all_words)
    bigram_freq = FreqDist(all_bigrams)

    # Combine unigrams and bigrams
    all_freq = unigram_freq + bigram_freq

    # Filter based on thresholds
    filtered_words = {
        word: freq
        for word, freq in all_freq.items()
        if freq >= threshold_2 and (freq / total_comments) <= threshold_1
    }

    # Sort the results and return the top 10
    sorted_words = sorted(filtered_words.items(),
                          key=lambda x: x[1], reverse=True)
    return sorted_words[:top_n]


def read_comments_from_csv(file_name):
    comments = []
    with open(file_name, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            comments.append(row['comments'])
    return comments

# Read comments from the CSV file


def is_english(text):
    try:
        language = detect(text)
        return language == "en"
    except LangDetectException:
        return False


comment_data = pd.read_csv("comment_data.csv", on_bad_lines='skip')
raw_comments = comment_data["comments"].tolist()

comments = [comment for comment in raw_comments if is_english(comment)]
print(len(comments))

# Get popular words/phrases
popular_words = get_popular_words(comments)
print(popular_words)
