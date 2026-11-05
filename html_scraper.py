from bs4 import BeautifulSoup, Tag


def _clean_text(tag: object) -> str:
    """Text of a tag with surrounding whitespace removed and inner runs collapsed.

    Unlike get_text(strip=True), this doesn't glue words together when inline
    tags such as <em> sit between whitespace-separated words.
    """
    return " ".join(tag.get_text().split()) if isinstance(tag, Tag) else ""


def get_heading_from_html(html: str) -> str:
    """Return the text of the first <h1>, falling back to the first <h2>.

    Returns an empty string if neither tag is present.
    """
    soup = BeautifulSoup(html, "html.parser")
    h_tag = soup.find("h1") or soup.find("h2")
    return _clean_text(h_tag)


def get_first_paragraph_from_html(html: str) -> str:
    """Return the text of the first <p>, preferring one inside <main>.

    If <main> exists but has no <p>, or <main> is absent, falls back to the
    first <p> in the document. Returns an empty string if there is no <p>.
    """
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find("main")
    p_tag = main.find("p") if isinstance(main, Tag) else None
    if p_tag is None:
        p_tag = soup.find("p")
    return _clean_text(p_tag)
