# https://rapidapi.com/winterfox/api/tiktok_solutions
# Trending Video/ Trending Videos by Region

import requests

url = "https://tiktok_solutions.p.rapidapi.com/trending/US"

# querystring = {"custom_cursor":"7035378109147596294"}

headers = {
    "X-RapidAPI-Key": "9b38cabe85mshb282f035a7bb13cp1fce86jsnc1693aca1d59",
    "X-RapidAPI-Host": "tiktok_solutions.p.rapidapi.com"
}

# response = requests.request("GET", url, headers=headers, params=querystring)
response = requests.request("GET", url, headers=headers)

# print(dir(response))

# ['__attrs__', '__bool__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__enter__', '__eq__', '__exit__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__nonzero__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__',
#     '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_content', '_content_consumed', '_next', 'apparent_encoding', 'close', 'connection', 'content', 'cookies', 'elapsed', 'encoding', 'headers', 'history', 'is_permanent_redirect', 'is_redirect', 'iter_content', 'iter_lines', 'json', 'links', 'next', 'ok', 'raise_for_status', 'raw', 'reason', 'request', 'status_code', 'text', 'url']

response_data = response.json()

if response_data['status'] == 'ok':
    for item in response_data['data']['list']:
        print(f"aweme_id: {item['aweme_id']}")
        print(f"creator_name: {item['author']['unique_id']}")
else:
    print("API returned an error")
