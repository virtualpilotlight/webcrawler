from urllib.parse import urlsplit



def normalize_url(url):
    finished = urlsplit(url)
    print(finished)
    return finished
