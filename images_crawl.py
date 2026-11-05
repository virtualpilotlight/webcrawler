from urllib.parse import urljoin

from bs4 import BeautifulSoup


def get_urls_from_html(html, base_url):
    """Return an un-normalized list of absolute URLs from every <a href> in html.

    Relative URLs are resolved against base_url. Anchors without an href are
    skipped. Raises ValueError if the HTML can't be parsed.
    """
    try:
        soup = BeautifulSoup(html, "html.parser")
    except Exception as e:
        raise ValueError(f"couldn't parse HTML: {e}") from e

    urls = []
    for anchor in soup.find_all("a"):
        href = anchor.get("href")
        if not href:
            continue
        try:
            urls.append(urljoin(base_url, href))
        except ValueError:
            # malformed URL (e.g. invalid IPv6 host); skip it
            continue
    return urls


def get_images_from_html(html, base_url):
    """Return an un-normalized list of absolute URLs from every <img src> in html.

    Relative URLs are resolved against base_url. Images without a src are
    skipped. Raises ValueError if the HTML can't be parsed.
    """
    try:
        soup = BeautifulSoup(html, "html.parser")
    except Exception as e:
        raise ValueError(f"couldn't parse HTML: {e}") from e

    urls = []
    for img in soup.find_all("img"):
        src = img.get("src")
        if not src:
            continue
        try:
            urls.append(urljoin(base_url, src))
        except ValueError:
            continue
    return urls
