from urllib.parse import urlparse, urlsplit

from get_html import get_html
from page_data import extract_page_data # <- adjust to wherever this lives


def normalize_url(url):
    url = url.strip()
    # urlsplit puts scheme-less URLs entirely in .path, so force a netloc
    if "//" not in url:
        url = "//" + url
    parts = urlsplit(url)
    host = (parts.hostname or "").lower()
    if parts.port:
        host = f"{host}:{parts.port}"
    path = parts.path.rstrip("/")
    return f"{host}{path}"


def crawl_page(base_url, current_url=None, page_data=None):
    if current_url is None:
        current_url = base_url
    if page_data is None:
        page_data = {}

    # Stay on the same domain
    if urlparse(current_url).netloc != urlparse(base_url).netloc:
        return page_data

    # Skip pages we've already crawled
    normalized = normalize_url(current_url)
    if normalized in page_data:
        return page_data

    print(f"Crawling: {current_url}")
    try:
        html = get_html(current_url)
    except Exception as e:
        print(f"  Failed to fetch {current_url}: {e}")
        return page_data

    data = extract_page_data(html, current_url)
    page_data[normalized] = data

    for link in data["outgoing_links"]:
        crawl_page(base_url, link, page_data)

    return page_data
