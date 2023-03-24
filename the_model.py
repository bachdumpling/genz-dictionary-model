import requests
import json
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import seaborn as sns
import matplotlib.pyplot as plt

api_key = "9b38cabe85mshb282f035a7bb13cp1fce86jsnc1693aca1d59"

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

        response_data = response.json()

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


def process_comments(comments):
    all_words = []
    for comment in comments:
        tokens = word_tokenize(comment)
        all_words.extend(tokens)

    fdist = FreqDist(all_words)
    return fdist


def visualize_top_words(fdist, top_n=10):
    df = pd.DataFrame(fdist.most_common(top_n), columns=['Word', 'Frequency'])
    sns.barplot(data=df, x='Word', y='Frequency')
    sns.despine()
    plt.show()


# video_ids = get_video_ids(api_key)
video_ids = ["7184827416517463342",
             "7197107078975049003"]
comments = get_comments(api_key, video_ids)
# print(comments)

fdist = process_comments(comments)
visualize_top_words(fdist)
