import pandas as pd
import nltk
import math
from nltk import word_tokenize
from nltk.util import ngrams
from collections import Counter
import string
from nltk.corpus import stopwords
import re
import json
from urllib.request import urlopen
from sklearn.feature_extraction.text import TfidfVectorizer


# Load the dataset
dataset = pd.read_csv("english_comments1.csv", on_bad_lines='skip')

# Preprocess the data
dataset['comments'] = dataset['comments'].str.lower()

# Remove emojis
def remove_emoji(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

dataset['comments'] = dataset['comments'].apply(remove_emoji)

# Tokenize the data
tokenized_comments = [word_tokenize(comment) for comment in dataset['comments']]

# Remove punctuation
def remove_punctuation(tokens):
    return [word for word in tokens if word not in string.punctuation]

tokenized_comments = [remove_punctuation(tokens) for tokens in tokenized_comments]

# Remove stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def remove_stopwords(tokens):
    return [word for word in tokens if word not in stop_words]

tokenized_comments = [remove_stopwords(tokens) for tokens in tokenized_comments]

# Get the function_words
function_words = json.loads(urlopen(
    "https://raw.githubusercontent.com/bachdumpling/genz-dictionary-model/main/function_words.json").read())

# Remove function words
def remove_function_words(tokens):
    return [word for word in tokens if word not in function_words]

tokenized_comments = [remove_function_words(tokens) for tokens in tokenized_comments]

# Calculate the Document Frequency (DF) of each word
def document_frequency(tokenized_comments):
    df = {}
    for tokens in tokenized_comments:
        unique_tokens = set(tokens)
        for token in unique_tokens:
            if token in df:
                df[token] += 1
            else:
                df[token] = 1
    return df

df = document_frequency(tokenized_comments)

# Calculate the Inverse Document Frequency (IDF) of each word
def inverse_document_frequency(df, total_documents):
    idf = {}
    for word, count in df.items():
        idf[word] = math.log10(total_documents / count)
    return idf

total_documents = len(tokenized_comments)
idf = inverse_document_frequency(df, total_documents)

# Filter words based on the given IDF threshold
idf_threshold = 0.9
filtered_words = [word for word, value in idf.items() if value >= idf_threshold]

# Recreate unigrams and calculate their frequency
unigrams = [ngrams(tokens, 1) for tokens in tokenized_comments]
unigrams_flat = [unigram for comment_unigrams in unigrams for unigram in comment_unigrams]

# Calculate the frequency of filtered unigrams
filtered_unigrams = [unigram for unigram in unigrams_flat if unigram[0] in filtered_words]
filtered_unigram_freq = Counter(filtered_unigrams)

# Sort the filtered unigram frequencies in descending order
sorted_filtered_unigram_freq = filtered_unigram_freq.most_common()

# Get the top 10 most frequent filtered unigrams
top_10_filtered_unigrams = sorted_filtered_unigram_freq[:10]

# Print the top 10 most frequent filtered unigrams
# print("Top 10 most frequent filtered words:")
# for rank, (unigram, count) in enumerate(top_10_filtered_unigrams, 1):
#     print(f"{rank}. {unigram[0]}: {count}")

# Create bigrams and calculate their frequency
bigrams = [ngrams(tokens, 2) for tokens in tokenized_comments]
bigrams_flat = [bigram for comment_bigrams in bigrams for bigram in comment_bigrams]

# Calculate the frequency of filtered bigrams
filtered_bigrams = [bigram for bigram in bigrams_flat if all(word in filtered_words for word in bigram)]
filtered_bigram_freq = Counter(filtered_bigrams)

# Sort the filtered bigram frequencies in descending order
sorted_filtered_bigram_freq = filtered_bigram_freq.most_common()

# Get the top 10 most frequent filtered bigrams
top_10_filtered_bigrams = sorted_filtered_bigram_freq[:10]

# Print the top 10 most frequent filtered bigrams
print("Top 10 most frequent filtered bigrams:")
for rank, (bigram, count) in enumerate(top_10_filtered_bigrams, 1):
    print(f"{rank}. {bigram[0]} {bigram[1]}: {count}")