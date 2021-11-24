from bs4 import BeautifulSoup
import requests
from CONST import DOWNLOADER_URL

def extract_download_links(tweet_url : str):

    data = {"tweet" : tweet_url, "csrfmiddlewaretoken" : ""}
    
    headers = {"referer" : "https://twittervideodownloader.com/",
    "origin" : "https://twittervideodownloader.com"}

    response = requests.get(DOWNLOADER_URL)
    doc = BeautifulSoup(response.text, 'html.parser')

    csrf = doc.find('form').find('input')['value']

    headers["cookie"] = "csrftoken=" + csrf

    data["csrfmiddlewaretoken"] = csrf

    post_url = DOWNLOADER_URL+"download"
    response = requests.post(post_url, data, headers=headers)

    post_doc = BeautifulSoup(response.text, 'html.parser')
    # downloadable_video = {'720p' : None, '480p' : None, '360p' : None}
    downloaded_video = None

    for a in post_doc.find_all('a', href=True):
        url = a['href']
        if 'vid' in url:
            if '1280x720' in url:
                downloadable_video = url

    return downloadable_video
    
