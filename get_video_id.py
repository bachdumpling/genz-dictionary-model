import requests
import json

url = "https://tiktok-all-in-one.p.rapidapi.com/feed"

headers = {
    "X-RapidAPI-Key": "9b38cabe85mshb282f035a7bb13cp1fce86jsnc1693aca1d59",
    "X-RapidAPI-Host": "tiktok-all-in-one.p.rapidapi.com"
}

# Initialize custom_cursor and request_limit
custom_cursor = ""
request_limit = 30
request_count = 0

# Initialize an empty list to store video IDs
video_ids = []

while request_count < request_limit:
    querystring = {"region": "US", "device_id": "7523368224928586621", "max_cursor": custom_cursor}

    response = requests.request("GET", url, headers=headers, params=querystring)
    response_data = response.json()

    if response_data['status_code'] == 0:
        for item in response_data['aweme_list']:
            video_ids.append(item['aweme_id'])

        # Check if there's a max_cursor value in the response and if it has more results
        if 'max_cursor' in response_data and response_data['has_more']:
            custom_cursor = str(response_data['max_cursor'])
        else:
            break
    else:
        print("API returned an error")
        break

    request_count += 1

# Write the video IDs to a JSON file
with open('video_ids2.json', 'w') as outfile:
    json.dump(video_ids, outfile)
