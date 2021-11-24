from functions import extract_download_links
url = "https://twitter.com/i/status/1463557722058592257"
l = extract_download_links(url)
if l is None:
    print("no video found!")
else:
    print(l)