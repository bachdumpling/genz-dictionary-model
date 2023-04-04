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


api_key = "9b38cabe85mshb282f035a7bb13cp1fce86jsnc1693aca1d59"

# Get the function_words
function_words = json.loads(urlopen(
    "https://raw.githubusercontent.com/bachdumpling/genz-dictionary-model/main/function_words.json").read())

# Get the stopwords and punctuation
nltk.download('stopwords')

stopwords = stopwords.words('english')
punctuation = list(punctuation)


def remove_emoji(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

# Get the video ids


def get_video_ids(api_key, region='US', request_limit=50):
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

        if response.status_code != 200:
            print(f"Error {response.status_code}: {response.text}")
            break

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


def get_comments(api_key, video_id_list, limit=100, offset=''):
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
            if data:  # Add this condition to check if data is not None
                for i, comment in enumerate(data):
                    if i < limit:  # Add this condition to limit the number of comments per video
                        comments.append(comment['text'])
                    else:
                        break
        except ValueError:
            print(
                f"Unexpected response for video ID {video_id}: {response.text}")

    return comments


def visualize_top_words(fdist, top_n=10):
    df = pd.DataFrame(fdist.most_common(top_n), columns=['Word', 'Frequency'])
    sns.barplot(data=df, x='Word', y='Frequency')
    sns.despine()
    plt.show()


# video_ids = json.loads(urlopen(
#     "https://raw.githubusercontent.com/bachdumpling/genz-dictionary-model/main/video_ids.json").read())
# video_ids = [
#     "7184827416517463342",
#     "7197107078975049003",
#     "7182232426884664618",
#     "7213402901819952427",
#     "7194449792225873195",
#     "7190353963588291841",
#     "7182902025955462446",
#     "7211900322447396138",
#     "7208202126663896366",
#     "7181306374331174187",
#     "7187890664040926506",
#     "7188341615164181806",
#     "7206085337100176682",
#     "7206103663364852998",
#     "7200426878073703722",
#     "7204592339388468481",
#     "7212091491706015022",
#     "7209159934733405486",
#     "7208168943771749637",
#     "7193375631370095918",
#     "7205291823231749419",
#     "7186492820453281070",
#     "7201610812732099883",
#     "7202712822642609454",
#     "7190124019369233665",
#     "7196184547598486830",
#     "7187083900810825002",
#     "7209671556044311854",
#     "7210634472037911815",
#     "7201311125932084523",
#     "7207930079144332590",
#     "7199003283845991726",
#     "7207989846533524779",
#     "7209059168244780334",
#     "7208720398949829934",
#     "7211498218654371073",
#     "7188571775297588526",
#     "7182016204230446382",
#     "7183225245829172526",
#     "7189655032017554693",
#     "7194920907901652229",
#     "7192183990961458478",
#     "7193495843821915435",
#     "7205639392491277611",
#     "7193767063062662442",
#     "7200398286874807594",
#     "7205744922262031659",
#     "7193805817915788587",
#     "7206896158789127466",
#     "7192032111883291946",
#     "7181554775647948075",
#     "7187168152625909038",
#     "7207149468607647018",
#     "7206472512203525418",
#     "7187133725656812843",
#     "7197525371380681989",
#     "7182614091125509418",
#     "7197358324566871302",
#     "7181267594916285738",
#     "7208751129813978414",
#     "7184568813202001194",
#     "7211523560362396974",
#     "7196879500825660718",
#     "7189271964085767429",
#     "7189094633404632363",
#     "7204252356731587882",
#     "7185679934159965486",
#     "7210254762749611310",
#     "7192295565323980074",
#     "7212191269899046150",
#     "7180487122493672706",
#     "7212807100299431214",
#     "7207810304334515499",
#     "7200216556519935237",
#     "7187500299270065451",
#     "7207036734394158338",
#     "7199708899077819654",
#     "7211267752806436097",
#     "7203433251321548074",
#     "7203864894356229422",
#     "7195087912956873989",
#     "7212433372969307434",
#     "7213006618861063470",
#     "7191624167282806059",
#     "7205927647379983658",
#     "7196000447864376618",
#     "7200937739825679662",
#     "7189718947376172293",
#     "7210877252106538282",
#     "7208758377755708718",
#     "7184273195921460523",
#     "7213028553783397678",
#     "7213206993581083950",
#     "7194933430885338410",
#     "7208530637983124737",
#     "7194982660702276906",
#     "7204899118785875243",
#     "7193815393285246254",
#     "7198679410181033258",]
# comments = ["That’s my favorite hole life savings lol",
            "Best story ever! I need a part 2 from baby!",
            "i love baby babble so much",
            "baby fever, Baby Fever, BABY FEVER!!!",
            "the wrist roll 😭😭😭 so cute",
            "babies listening to their own voices is just so cute!",
            "It's funny to think about how babies probably don't know when they say their first word because they probably think they're talking all the time.",
            "Omg her covering her mouth while yawning… ugh adorable ☺️",
            "That was the most in depth story ever! I was hooked",
            "that's how her day went😂😂",
            "the covering her mouth for the yawn 🥺❤️",
            "i love baby voices 🥺🥺",
            "oh my goodness she is so precious U0001f979",
            "The caption U0001f979U0001f979",
            "🥱🥱🥱oh my goodness🥰🥰🥰",
            "it's like she's telling a very serious story about dada!😂😂🥰🥰🥰",
            "I don’t want another baby i don’t want another baby i don’t want another baby 😂😂😩😩😩😩",
            "her covering her yawn 🥺",
            "OMG . So cute 🥰🥰",
            "She is so adorable!!",
            "Oh no she covered her mouth yawning!!!! That is so cute",]

video_ids = get_video_ids(api_key)
comments = get_comments(api_key, video_ids)

print("# of video ids: ", len(video_ids))
print("# of video comments: ", len(comments))

result = []

stopwords = set(stopwords)
function_words = set(function_words)
punctuation = set(punctuation)


def combo(sentence):
    print("sentence before:", sentence)

    sentence = re.sub(r'[^\w\s]', '', sentence)
    sentence = remove_emoji(sentence)

    print("sentence after:", sentence)

    duplicated_tokens = word_tokenize(sentence)
    tokens = list(set(duplicated_tokens))

    print("dirty tokens:", tokens)

    accepted_list = []

    translator = str.maketrans('', '', string.punctuation)

    cleaned_tokens = [
        token.lower()
        for token in tokens
        if token.lower() not in stopwords
        and token.lower() not in function_words
        and token.lower() not in punctuation
    ]

    print("clean tokens:", cleaned_tokens)

    accepted_list.append(cleaned_tokens)

    combinations = []
    # for i in range(len(cleaned_tokens)):
    #     for j in range(i+1, len(cleaned_tokens)+1):
    #         combinations.append(" ".join(cleaned_tokens[i:j]))

    for i in range(len(cleaned_tokens)):
        for j in range(i+1, len(cleaned_tokens)+1):
            if j - i > 1:  # Add this condition to only add combinations with more than one token
                combinations.append(" ".join(cleaned_tokens[i:j]))
    print("combinations", combinations)

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
visualize_top_words(freq_dist, 10)
