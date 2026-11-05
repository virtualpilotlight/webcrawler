import requests


def get_html(url):
    try:
        response = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})
    except requests.RequestException as e:
        raise Exception(f"network error while fetching {url}: {e}")

    if response.status_code >= 400:
        raise Exception(f"got HTTP error: {response.status_code} {response.reason}")

    content_type = response.headers.get("content-type", "")
    if "text/html" not in content_type:
        raise Exception(f"non-HTML response: content-type is '{content_type}'")

    return response.text
