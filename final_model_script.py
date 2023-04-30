# %%
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
from collections import Counter

api_key = "9b38cabe85mshb282f035a7bb13cp1fce86jsnc1693aca1d59"

# %%
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

# %%
comment_data = pd.read_csv("english_comments1.csv", on_bad_lines='skip')

# raw_comments = comment_data["comments"].tolist()
dirty_comments = comment_data["comments"].tolist()

#clean:
comments = []
for comment in dirty_comments:
    comment = re.sub(r'[^\w\s]', '', comment)
    comment = remove_emoji(comment)
    print(comment)
    comments.append(comment)


print(comments)
print(len(comments))

# %%
def train_unigram_model(corpus):
    words = [word.lower() for sentence in corpus for word in word_tokenize(sentence)]
    unigram_freq = Counter(words)
    return unigram_freq

def train_bigram_model(corpus):
    words = [word.lower()
             for sentence in corpus for word in word_tokenize(sentence)]
    bigram_measures = BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(words)
    finder.apply_freq_filter(4)
    scored_bigrams = finder.score_ngrams(bigram_measures.pmi)
    return dict(scored_bigrams)

unigram_model = train_unigram_model(comments)
bigram_model = train_bigram_model(comments)
print(bigram_model)

def calculate_combinations(cleaned_tokens, unigram_model, bigram_model, unigram_threshold, bigram_threshold):
    filtered_combinations = []

    for i in range(len(cleaned_tokens)):
        for j in range(i+1, len(cleaned_tokens)+1):
            if j - i == 2:  # Bigram case
                bigram = tuple(cleaned_tokens[i:j])
                # print(" ".join(bigram))
                if bigram in bigram_model:
                    bigram_pmi = bigram_model[bigram]
                    print("bigram:", bigram, bigram_pmi)
                    if bigram_pmi > bigram_threshold:
                        filtered_combinations.append(" ".join(bigram))
                        # print(" ".join(bigram))
            # if j - i == 1:  # Unigram case
            #     unigram = cleaned_tokens[i]
            #     unigram_freq = unigram_model.get(unigram, 0)
            #     if unigram_freq <= unigram_threshold:
            #         filtered_combinations.append(unigram)
    print(filtered_combinations)
    return filtered_combinations

def idf(word, comments):
    num_docs_with_word = sum(
        1 for comment in comments if word in comment.lower())
    return math.log(len(comments) / (1 + num_docs_with_word))
    

# %%
bigram_threshold = 12
unigram_threshold = 20

result = []

def combo(sentence, comments):
    sentence = re.sub(r'[^\w\s]', '', sentence)
    sentence = remove_emoji(sentence)

    duplicated_tokens = word_tokenize(sentence)
    tokens = list(set(duplicated_tokens))

    cleaned_tokens = [
        token.lower()
        for token in tokens
        if token.lower() not in stopwords
        and token.lower() not in function_words
        and token.lower() not in punctuation
    ]

    # print(cleaned_tokens)

    combinations = calculate_combinations(
        cleaned_tokens, unigram_model, bigram_model, unigram_threshold, bigram_threshold)
    
    top_words = [word for word in combinations]
    result.append(top_words)

for comment in comments:
    combo(comment, comments)

# %%
# Define a function to visualize the top words in a frequency distribution
def visualize_top_words(fdist, top_n=10):
    # Create a DataFrame with the top_n words and their frequencies
    df = pd.DataFrame(fdist.most_common(top_n), columns=['Word', 'Frequency'])
    
    # Check if the DataFrame is empty
    if df.empty:
        print("No top words found.")
    else:
        # Create a horizontal bar plot of the top words and their frequencies
        sns.barplot(data=df, x='Frequency', y='Word')
        # Remove the top and right spines of the plot for a cleaner appearance
        sns.despine()
        # Display the generated plot
        plt.show()

# Flatten the nested list 'result'
flat_result = []
for sublist in result:
    for item in sublist:
        flat_result.append(item)

# Create a frequency distribution from the flattened list
freq_dist = FreqDist(flat_result)

# Print and visualize the 10 most common words in the frequency distribution
print(freq_dist.most_common(20))
visualize_top_words(freq_dist, 20)

# Print the flattened list
print(flat_result)

# Calculate the IDF values for each word in the flattened list
idf_values = {}
for word in flat_result:
    if word not in idf_values:
        idf_values[word] = idf(word, comments)

# Sort the IDF values in descending order
sorted_idf_values = sorted(idf_values.items(), key=lambda x: x[1], reverse=True)

# Print the sorted IDF values
print(sorted_idf_values)

# Create an IDF-weighted frequency distribution
idf_weighted_freq_dist = FreqDist({word: freq * idf_values[word] for word, freq in freq_dist.items()})

# Print and visualize the 20 most common words in the IDF-weighted frequency distribution
print(idf_weighted_freq_dist.most_common(20))
visualize_top_words(idf_weighted_freq_dist, 20)


