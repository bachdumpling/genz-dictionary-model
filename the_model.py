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

api_key = "9b38cabe85mshb282f035a7bb13cp1fce86jsnc1693aca1d59"

# Get the function_words
function_words = json.loads(urlopen(
    "https://raw.githubusercontent.com/bachdumpling/genz-dictionary-model/main/function_words.json").read())

# Get the stopwords and punctuation
nltk.download('stopwords')

stopwords = set(stopwords.words('english'))
extra_words = {
    'im', 'dont', 'bc', 'na',
    'see', 'would', 'time', 'every',
    'go', 'like', 'going', 'right',
    'back', 'looks',
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves',
    'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves',
    'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself',
    'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
    'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those',
    'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
    'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after',
    'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
    'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
    's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didnt', "didn't", 'doesnt', "doesn't", 'hadnt', "hadn't", 'hasnt', "hasn't", 'havent', "haven't", 'isnt', "isn't", 'ma', 'mightnt', "mightn't", 'mustnt', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldnt', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't",
    'bro', 'way', 'much', 'know', 'said', 'people', 'hes', 'got', 'comments', 'eyes', 'thank', 'love', 'oh', 'make', 'school', 'use', 'talking', 'videos', 'family', 'name',   'hello', 'goodbye', 'please', 'thank', 'yes', 'no', 'maybe', 'sure',
    'morning', 'afternoon', 'evening', 'night', 'today', 'tomorrow', 'yesterday',
    'work', 'job', 'office', 'home', 'house', 'apartment', 'family', 'friend', 'partner',
    'eat', 'drink', 'food', 'breakfast', 'lunch', 'dinner', 'snack', 'meal',
    'happy', 'sad', 'angry', 'excited', 'tired', 'bored', 'surprised', 'worried',
    'school', 'college', 'university', 'class', 'teacher', 'student', 'study', 'learn',
    'car', 'bus', 'train', 'bike', 'walk', 'drive', 'ride', 'transportation', 'vehicle', 'isnt', 'seen',
    'one', 'get', 'say', 'good', 'feel', 'first', 'someone', 'thought', 'water', 'person', 'baby', 'whats', 'done', 'cat', 'ive', 'us', 'next', 'thing', 'something', 'could'
}

stopwords.update(extra_words)

punctuation = list(punctuation)


def remove_emoji(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)


def visualize_top_words(fdist, top_n=10):
    df = pd.DataFrame(fdist.most_common(top_n), columns=['Word', 'Frequency'])
    sns.barplot(data=df, x='Frequency', y='Word')  # Switch x and y parameters
    sns.despine()
    plt.yticks(rotation=0)  # Set y-axis labels to be horizontal
    plt.show()


def is_english(text):
    try:
        language = detect(text)
        return language == "en"
    except LangDetectException:
        return False


comment_data = pd.read_csv("comment_data.csv")
raw_comments = comment_data["comments"].tolist()

comments = [comment for comment in raw_comments if is_english(comment)]
print(len(comments))

result = []

stopwords = set(stopwords)
function_words = set(function_words)
punctuation = set(punctuation)


def combo(sentence):
    # print("sentence before:", sentence)

    sentence = re.sub(r'[^\w\s]', '', sentence)
    sentence = remove_emoji(sentence)

    # print("sentence after:", sentence)

    duplicated_tokens = word_tokenize(sentence)
    tokens = list(set(duplicated_tokens))

    # print("dirty tokens:", tokens)

    accepted_list = []

    translator = str.maketrans('', '', string.punctuation)

    cleaned_tokens = [
        token.lower()
        for token in tokens
        if token.lower() not in stopwords
        and token.lower() not in function_words
        and token.lower() not in punctuation
    ]

    # print("clean tokens:", cleaned_tokens)

    accepted_list.append(cleaned_tokens)

    combinations = []
    # for i in range(len(cleaned_tokens)):
    #     for j in range(i+1, len(cleaned_tokens)+1):
    #         combinations.append(" ".join(cleaned_tokens[i:j]))

    for i in range(len(cleaned_tokens)):
        for j in range(i+1, len(cleaned_tokens)+1):
            if j - i > 1 and j - i < 3:  # Add this condition to only add combinations with more than one token
            # if j - i == 1:  # Change this condition to only add combinations with exactly one token
                combinations.append(" ".join(cleaned_tokens[i:j]))

    # calculate the frequency distribution of the words
    freq_dist = FreqDist(combinations)

    # determine the number of unique words in the text
    num_unique_words = len(freq_dist)

    # calculate the number of words to include in the top 25%
    num_top_words = int(num_unique_words * 0.10)

    # construct a list of the top 25% most common words
    top_words = [word for word, freq in freq_dist.most_common(num_top_words)]
    result.append(top_words)


for comment in comments:
    combo(comment)

flat_result = []

for sublist in result:
    for item in sublist:
        flat_result.append(item)

freq_dist = FreqDist(flat_result)

print(freq_dist.most_common(10))
visualize_top_words(freq_dist, 10)
