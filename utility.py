from decouple import config
import requests
import logging
def bearer_oauth(r):
    bearer_token = config('BEARER_TOKEN', 'AAAAAAAAAAAAAAAAAAAAAP2PowEAAAAAFcHqjQSiK8bGjz8OrO1GurUth8k%3DSfyS3VE7Q2dMK4mUsqjkniru0nwr6edWikvs3K4tUTkPrWbaxJ')
    r.headers["Authorization"] = f"Bearer {bearer_token}"
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
    logging.error(result)
    return None


def get_HDVideo(media):
    video_url = None

    for item in media:
        media_type = item["type"]

        # ignore other media except video
        if media_type != "video":
            continue

        # get all video qualities
        variants = item["variants"]

        # get max video quality
        max_bit_rate = 0
        for v in variants:
            if v["content_type"] == "video/mp4":
                if v["bit_rate"] > max_bit_rate:
                    video_url = v["url"]
    
    return video_url
