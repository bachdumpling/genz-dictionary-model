#https://rapidapi.com/h0p3rwe/api/tiktok-all-in-one
import requests

id_list = [7205233664635063594, 7205941414524505387, 7180997355624205614, 7206905041850993963,
           7174768208090516778, 7174565510158322987, 7185745477130816811, 7206363628101045547]

url = "https://tiktok-all-in-one.p.rapidapi.com/video/comments"
# only need to change the offset and keep the same for all ids
querystring = {"offset": ""}

headers = {
    "X-RapidAPI-Key": "9b38cabe85mshb282f035a7bb13cp1fce86jsnc1693aca1d59",
    "X-RapidAPI-Host": "tiktok-all-in-one.p.rapidapi.com"
}

comments = []

for video_id in id_list:
    querystring = {"id": video_id}
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()["comments"]
    for comment in data:
        comments.append(comment['text'])

print(len(comments))
