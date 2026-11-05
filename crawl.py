from urllib.parse import urlsplit


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
