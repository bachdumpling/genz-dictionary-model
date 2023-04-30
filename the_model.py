from string import punctuation
from nltk.corpus import stopwords
import requests
import json
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import seaborn as sns
import matplotlib.pyplot as plt
from urllib.request import urlopen
from string import punctuation
import string
import re
from langdetect import detect, LangDetectException
import math
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder
from nltk.util import ngrams

api_key = "9b38cabe85mshb282f035a7bb13cp1fce86jsnc1693aca1d59"

# Get the function_words
function_words = json.loads(urlopen(
    "https://raw.githubusercontent.com/bachdumpling/genz-dictionary-model/main/function_words.json").read())

# Get the stopwords and punctuation
nltk.download('stopwords')

stopwords = set(stopwords.words('english'))

punctuation = list(punctuation)


def remove_emoji(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)


def idf(word, comments):
    num_docs_with_word = sum(
        1 for comment in comments if word in comment.lower())
    return math.log(len(comments) / (1 + num_docs_with_word))


def visualize_top_words(fdist, top_n=10):
    df = pd.DataFrame(fdist.most_common(top_n), columns=['Word', 'Frequency'])
    if df.empty:
        print("No top words found.")
    else:
        sns.barplot(data=df, x='Frequency', y='Word')
        sns.despine()
        plt.show()


def train_bigram_model(corpus):
    words = [word.lower()
             for sentence in corpus for word in word_tokenize(sentence)]
    bigram_measures = BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(words)
    finder.apply_freq_filter(2)
    scored_bigrams = finder.score_ngrams(bigram_measures.pmi)
    return dict(scored_bigrams)


def calculate_combinations(cleaned_tokens, bigram_model, threshold):
    filtered_combinations = []

    for i in range(len(cleaned_tokens)):
        for j in range(i+1, len(cleaned_tokens)+1):
            if j - i == 2:
                bigram = tuple(cleaned_tokens[i:j])
                if bigram in bigram_model and bigram_model[bigram] > threshold:
                    filtered_combinations.append(" ".join(bigram))

    return filtered_combinations


comment_data = pd.read_csv("english_comments1.csv", on_bad_lines='skip')
# raw_comments = comment_data["comments"].tolist()
comments = comment_data["comments"].tolist()

# comments = [comment for comment in raw_comments if is_english(comment)]
print(len(comments))


bigram_model = train_bigram_model(comments)
pmi_threshold = 1
stopwords = set(stopwords)
function_words = set(function_words)
punctuation = set(punctuation)

result = []


def combo(sentence, comments):
    # print("sentence before:", sentence)

    sentence = re.sub(r'[^\w\s]', '', sentence)
    sentence = remove_emoji(sentence)

    # print("sentence after:", sentence)

    duplicated_tokens = word_tokenize(sentence)
    tokens = list(set(duplicated_tokens))

    # print("dirty tokens:", tokens)

    translator = str.maketrans('', '', string.punctuation)

    cleaned_tokens = [
        token.lower()
        for token in tokens
        if token.lower() not in stopwords
        and token.lower() not in function_words
        and token.lower() not in punctuation
    ]

    # print("clean tokens:", cleaned_tokens)

    combinations = calculate_combinations(
        cleaned_tokens, bigram_model, pmi_threshold)

    idf_threshold = math.log(len(comments) * 0.2)

    filtered_combinations = [word for word in combinations if idf(
        word, comments) > idf_threshold]

    # print(combinations)

    # calculate the frequency distribution of the words
    freq_dist = FreqDist(filtered_combinations)

    # determine the number of unique words in the text
    num_unique_words = len(freq_dist)

    # calculate the number of words to include in the top 25%
    num_top_words = int(num_unique_words * 0.9)

    # construct a list of the top 25% most common words
    top_words = [word for word, freq in freq_dist.most_common(num_top_words)]
    result.append(top_words)


for comment in comments:
    combo(comment, comments)


flat_result = []

for sublist in result:
    for item in sublist:
        flat_result.append(item)

freq_dist = FreqDist(flat_result)

print(freq_dist.most_common(10))
visualize_top_words(freq_dist, 10)

