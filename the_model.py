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


api_key = "9b38cabe85mshb282f035a7bb13cp1fce86jsnc1693aca1d59"

# Get the function_words
function_words = json.loads(urlopen(
    "https://raw.githubusercontent.com/bachdumpling/genz-dictionary-model/main/function_words.json").read())

# Get the stopwords and punctuation
nltk.download('stopwords')

stopwords = stopwords.words('english')
punctuation = list(punctuation)

# Get the video ids


def get_video_ids(api_key, region='US', request_limit=10):
    url = "https://tiktok-all-in-one.p.rapidapi.com/feed"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "tiktok-all-in-one.p.rapidapi.com"
    }

    custom_cursor = ""
    request_count = 0

    video_ids = []

    while request_count < request_limit:
        querystring = {
            "region": region, "device_id": "7523368224928586621", "max_cursor": custom_cursor}
        response = requests.request(
            "GET", url, headers=headers, params=querystring)

        try:
            response_data = response.json()
        except ValueError:
            print("Response content:", response.content)
            raise Exception("Unable to parse response content as JSON")

        if response_data['status_code'] == 0:
            for item in response_data['aweme_list']:
                video_ids.append(item['aweme_id'])

            if 'max_cursor' in response_data and response_data['has_more']:
                custom_cursor = str(response_data['max_cursor'])
            else:
                break
        else:
            print("API returned an error")
            break

        request_count += 1

    return video_ids


def get_comments(api_key, video_id_list, offset=''):
    url = "https://tiktok-all-in-one.p.rapidapi.com/video/comments"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "tiktok-all-in-one.p.rapidapi.com"
    }

    comments = []

    for video_id in video_id_list:
        querystring = {"id": video_id, "offset": offset}
        response = requests.request(
            "GET", url, headers=headers, params=querystring)
        try:
            data = response.json()["comments"]
            for comment in data:
                comments.append(comment['text'])
        except ValueError:
            print(
                f"Unexpected response for video ID {video_id}: {response.text}")

    return comments


# def process_comments(comments):
#     all_words = []
#     for comment in comments:
#         tokens = word_tokenize(comment)
#         all_words.extend(tokens)

#     fdist = FreqDist(all_words)
#     return fdist


def visualize_top_words(fdist, top_n=10):
    df = pd.DataFrame(fdist.most_common(top_n), columns=['Word', 'Frequency'])
    sns.barplot(data=df, x='Word', y='Frequency')
    sns.despine()
    plt.show()


# video_ids = get_video_ids(api_key)
video_ids = json.loads(urlopen(
    "https://raw.githubusercontent.com/bachdumpling/genz-dictionary-model/main/video_ids.json").read())
comments = get_comments(api_key, video_ids)
# print(comments)

# fdist = process_comments(comments)
# print(fdist.most_common(10))
result = []


def combo(sentence):
    duplicated_tokens = word_tokenize(sentence)
    tokens = list(set(duplicated_tokens))
    accepted_list = []

    translator = str.maketrans('', '', string.punctuation)

    #   cleaned_tokens = [token for token in tokens if token not in stopwords or token not in functionWords and token not in punctuation]
    cleaned_tokens = [token.lower() for token in tokens if token.lower(
    ) not in stopwords and token.lower() not in function_words and token.lower() not in punctuation]

    accepted_list.append(cleaned_tokens)

    combinations = []
    for i in range(len(cleaned_tokens)):
        for j in range(i+1, len(cleaned_tokens)+1):
            combinations.append(" ".join(cleaned_tokens[i:j]))
    # calculate the frequency distribution of the words
    freq_dist = FreqDist(combinations)

    # determine the number of unique words in the text
    num_unique_words = len(freq_dist)

    # calculate the number of words to include in the top 25%
    num_top_words = int(num_unique_words * 0.25)

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

# visualize_top_words(freq_dist)
