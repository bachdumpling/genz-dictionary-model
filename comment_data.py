import requests
import csv
import time
import os


def get_video_ids(api_key, region='US', request_limit=200):
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
                        comments.append((video_id, comment['text']))
                    else:
                        break
        except ValueError:
            print(
                f"Unexpected response for video ID {video_id}: {response.text}")

    return comments


def main():
    api_key = "9b38cabe85mshb282f035a7bb13cp1fce86jsnc1693aca1d59"
    comment_count = 0
    file_exists = os.path.isfile("comment_data.csv")

    with open("comment_data.csv", "a", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["videoid", "comments"])
        
        # Only write the header if the file doesn't exist
        if not file_exists:
            csv_writer.writerow(["videoid", "comments"])

        while comment_count < 10000:
            video_ids = get_video_ids(api_key)
            comments = get_comments(api_key, video_ids)
            print(len(video_ids))

            for video_id, comment in comments:
                csv_writer.writerow([video_id, comment])
                comment_count += 1

                if comment_count >= 10000:
                    break

            time.sleep(1)


if __name__ == "__main__":
    main()
