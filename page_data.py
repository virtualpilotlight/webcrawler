from typing import TypedDict
from urllib.parse import urljoin

from bs4 import BeautifulSoup


class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]


def get_heading_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in ("h1", "h2"):
        el = soup.find(tag)
        if el:
            return el.get_text(strip=True)
    return ""


def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find("main")
    p = main.find("p") if main else None
    if p is None:
        p = soup.find("p")
    return p.get_text(strip=True) if p else ""


def get_urls_from_html(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    return [
        urljoin(base_url, a["href"])
        for a in soup.find_all("a", href=True)
    ]


def get_images_from_html(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    return [
        urljoin(base_url, img["src"])
        for img in soup.find_all("img", src=True)
    ]


def extract_page_data(html: str, page_url: str) -> PageData:
    return {
        "url": page_url,
        "heading": get_heading_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, page_url),
        "image_urls": get_images_from_html(html, page_url),
    }
