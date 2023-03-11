import requests
from itertools import chain, combinations

# comment_list = [
#     "I swear I thought the stork actually rang the bell until o saw the baby and got the joke😂😂😂 cause after what I’ve seen animals can do now phewww😂",
#     "am I the only one wondering how she did this?!",
#     "You gotta number for that stork, cause i want one.",
#     "Omg how cute is this!!! When she/he asks where I came from you have proof",
#     "so cute🥰",
#     "This is amazing",
#     "You can order them on Amazon and they send it to your door along with the baby",
#     "My stork was lost for many years. Thankfully they found their way to my home 💕. This is just so precious 🥺",
#     "I KNEW THATS HOW IT HAPPENS!!!!"]

comment_list = [
    "I swear I thought the stork actually rang the bell until o saw the baby and got the joke😂😂😂 cause after what I’ve seen animals can do now phewww😂",
    "am I the only one wondering how she did this?!"]

collected_words = []


def collectingWords(commentData):
    # Loop through the comments and create a power set of each sentence
    power_sets = []

    for sentence in commentData:
        # Split the sentence into an array of single words
        words = sentence.split()

        # Create a power set array (What if the words appear multiple times in the same sentence?)
        power_set = list(chain.from_iterable(combinations(words, r)
                         for r in range(len(words)+1)))
        power_sets.append(power_set)

    # Flatten the power_sets list
    output = list(chain.from_iterable(power_sets))

    # Concatenate each element in the power set array into strings
    output = [' '.join(subset) for subset in output]

    # Match the strings in the array to the Urban Dictionary API
    url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
    api_key = 'your-api-key'
    headers = {
        "X-RapidAPI-Key": "9b38cabe85mshb282f035a7bb13cp1fce86jsnc1693aca1d59",
        "X-RapidAPI-Host": "mashape-community-urban-dictionary.p.rapidapi.com"
    }

    accepted_words = []

    for string in output:
        querystring = {"term": string}
        # Make the API request with the string and headers
        response = requests.get(url, headers=headers, params=querystring)
        # Check if the response is successful (status code 200)
        if response.status_code == 200:
            # Check if the string exists in the dictionary database
            if response.json().get('list'):
                if response.json().get('list')[0].get('word').lower() == string.lower():
                    accepted_words.append(string)

    return accepted_words


print(collectingWords(comment_list))
