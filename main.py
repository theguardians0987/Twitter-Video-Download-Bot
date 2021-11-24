import requests
from bs4 import BeautifulSoup

DOWNLOADER_URL = "https://twittervideodownloader.com/"
video_url = "https://twitter.com/i/status/1463475202646429702"

def main(url):
    data = {"tweet" : video_url, "csrfmiddlewaretoken" : ""}
    headers = {"referer" : "https://twittervideodownloader.com/",
    "origin" : "https://twittervideodownloader.com"}

    response = requests.get(url)
    doc = BeautifulSoup(response.text, 'html.parser')
    
    csrf = doc.find('form').find('input')['value']
    headers["cookie"] = "csrftoken=" + csrf
    data["csrfmiddlewaretoken"] = csrf

    post_url = "https://twittervideodownloader.com/download"
    response = requests.post(post_url, data, headers=headers)

    post_doc = BeautifulSoup(response.text, 'html.parser')
    downloadable_video = []

    for a in post_doc.find_all('a', href=True):
        if 'vid' in a['href'] :
            downloadable_video.append(a['href'])

    print(downloadable_video)

main(DOWNLOADER_URL)