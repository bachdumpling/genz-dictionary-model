import requests
import string
import time
from itertools import chain, combinations

functionWords = [
    "a",
    "an",
    "the",
    "and",
    "but",
    "or",
    "as",
    "if",
    "when",
    "than",
    "because",
    "though",
    "although",
    "while",
    "where",
    "after",
    "before",
    "since",
    "until",
    "by",
    "with",
    "without",
    "under",
    "over",
    "in",
    "on",
    "at",
    "to",
    "from",
    "into",
    "onto",
    "out",
    "off",
    "up",
    "down",
    "through",
    "around",
    "about",
    "above",
    "below",
    "near",
    "far",
    "along",
    "across",
    "behind",
    "beside",
    "between",
    "beyond",
    "inside",
    "outside",
    "throughout",
    "toward",
    "towards",
    "via",
    "among",
    "amongst",
    "within",
    "without",
    "ago",
    "now",
    "just",
    "already",
    "still",
    "even",
    "only",
    "almost",
    "nearly",
    "perhaps",
    "maybe",
    "certainly",
    "surely",
    "really",
    "truly",
    "sincerely",
    "actually",
    "definitely",
    "practically",
    "ultimately",
    "basically",
    "generally",
    "mostly",
    "often",
    "sometimes",
    "rarely",
    "seldom",
    "never",
    "ever",
    "always",
    "together",
    "apart",
    "thus",
    "therefore",
    "hence",
    "so",
    "then",
    "nowadays",
    "meanwhile",
    "forthwith",
    "later",
    "sooner",
    "instead",
    "nevertheless",
    "however",
    "furthermore",
    "moreover",
    "in addition",
    "in contrast",
    "in fact",
    "indeed",
    "that",
    "what",
    "which",
    "who",
    "whom",
    "whose",
    "where",
    "when",
    "why",
    "how",
]

# Import the json results file from the Google Sheet CSV export
# result = ["such a cutie pie", "such a cutie pie"]

# Loop through the results and create a power set of each sentence
# dirty_sentence = "such a cutie pie 💀"
dirty_sentence = "She is so adorable!! 🥰"
print("1. Given sentence: ", dirty_sentence)

# power_set of sentence
# power_set = ["such", "a", "cutie", "pie", "such a", "such cutie", "such pie", "a cutie", "a pie", "cutie pie", "such a cutie", "such a pie", "such cutie pie", "a cutie pie", "such a cutie pie"]
#  run freqdist, remove the tail

# Remove all punctuations before splitting the sentence into an array of words
translator = str.maketrans('', '', string.punctuation)
sentence = dirty_sentence.translate(translator).lower()
print("\n2. Cleaning the sentence: ", sentence)

# Split the sentence into an array of single words
words = sentence.split()
print("\n3. Split the sentence into an array of single words: words = ", words)

# Create a power set array (What if the words appear multiple times in the same sentence?)
power_set = list(chain.from_iterable(combinations(words, r)
                 for r in range(len(words)+1)))
print("\n4. Create a power set array: power_set = ", power_set)

# Concatenate each element in the power set array into strings
output = [' '.join(subset) for subset in power_set]
print("\n5. Create possible words from the power set: output = ", output)

# Match the strings in the array to the Urban Dictionary API
url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
api_key = 'your-api-key'
headers = {
    "X-RapidAPI-Key": "9b38cabe85mshb282f035a7bb13cp1fce86jsnc1693aca1d59",
    "X-RapidAPI-Host": "mashape-community-urban-dictionary.p.rapidapi.com"
}

# querystring = {"term":"cutie pie"}

# response = requests.request("GET", url, headers=headers, params=querystring)

# print(response.json().get('list')[0].get('word'))

accepted_words = []
print("\n6. Match the words in the 'output' list to the Urban Dictionary API: ")

# Loop through the output list and make API requests
for i, string in enumerate(output):
    # Print the loading message with the current iteration number
    print(f"Loading... {i+1}/{len(output)}", end="\r")

    # Make the API request with the string and headers
    querystring = {"term": string}
    response = requests.get(url, headers=headers, params=querystring)

    # Check if the response is successful (status code 200)
    if response.status_code == 200:
        # Check if the string exists in the dictionary database
        if response.json().get('list'):
            if response.json().get('list')[0].get('word').lower() == string.lower():
                accepted_words.append(string)
    else:
        print(f"Error: Failed to connect to the API for string {string}.")

    # Simulate a delay of 1 second between each iteration of the loop
    time.sleep(1)

print("\nDone!")

# If the function words in "accepted_words" are single words, remove them from the array
accepted_words = [word for word in accepted_words if word not in functionWords]
print("\nMatched words: ",accepted_words)

wordCounts = {}

for word in accepted_words:
    if word in wordCounts:
        wordCounts[word] += 1
    else:
        wordCounts[word] = 1

print("\n7. Return the frequency of each words: ")
for word, count in wordCounts.items():
    print(f"{word}: {count}")


# How to reduce run time and improve efficiency of the model?