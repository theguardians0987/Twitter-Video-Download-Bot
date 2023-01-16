import requests
import os

def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {os.environ['BEARER_TOKEN']}"
    r.headers["User-Agent"] = "v2TweetLookupPython"
    return r

def get_tweet(url):
    id = url.split('?')[0].split("/")[-1]
    expansions = "attachments.media_keys"
    media_fields = "type,url,preview_image_url,variants"
    endpoint = "https://api.twitter.com/2/" + f"tweets?ids={id}&expansions={expansions}&media.fields={media_fields}"
    response = requests.request("GET", endpoint, auth=bearer_oauth)   
    result = response.json()
    if response.status_code == 200 and result.get("errors", None) == None:
        return result
    return None
    


r = get_tweet("https://twitter.com/introvertsmemes/status/1614951522671927291")
print(r)
