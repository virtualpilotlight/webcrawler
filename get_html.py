import requests


async def get_html(url, url):
    try:
        async with self.session.get(
            url, headers={"User-Agent": "BootCrawler/1.0"}
        ) as response:
            if response.status >= 400:
                raise Exception(f"got HTTP error: {response.status_code} {response.reason}")

            content_type = response.headers.get("content-type", "")
            if "text/html" not in content_type:
                raise Exception(f"non-HTML response: content-type is '{content_type}'")

            return await response.text()
    except aiohttp.ClientError as e:
        raise Exception(f"network error while fetching {url}: {e}")
