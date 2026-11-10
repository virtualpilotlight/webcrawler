import asyncio
from urllib.parse import urlparse, urlsplit

import aiohttp

from page_data import extract_page_data


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


class AsyncCrawler:
    def __init__(self, base_url, max_concurrency, max_pages):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.page_data = {}
        self.visited = set()
        self.lock = asyncio.Lock()
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.session = None
        self.max_pages = max_pages
        self.should_stop = False
        self.all_tasks = set()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if self.should_stop:
                return False

            if len(self.visited) >= self.max_pages:
                self.should_stop = True
                print("Reached maximum number of pages to crawl.")
                return False

            if normalized_url in self.visited:
                return False

            self.visited.add(normalized_url)
            return True

    async def get_html(self, url):
        try:
            async with self.session.get(
                url, headers={"User-Agent": "BootCrawler/1.0"}
            ) as response:
                if response.status >= 400:
                    raise Exception(
                        f"got HTTP error: {response.status} {response.reason}"
                    )

                content_type = response.headers.get("content-type", "")
                if "text/html" not in content_type:
                    raise Exception(
                        f"non-HTML response: content-type is '{content_type}'"
                    )

                return await response.text()
        except aiohttp.ClientError as e:
            raise Exception(f"network error while fetching {url}: {e}")

    async def crawl_page(self, current_url):
        if self.should_stop:
            return

        # Same-domain check comes before recording a visit or fetching
        if urlparse(current_url).netloc != self.base_domain:
            return

        normalized = normalize_url(current_url)
        if not await self.add_page_visit(normalized):
            return

        async with self.semaphore:
            print(f"Crawling: {current_url}")
            try:
                html = await self.get_html(current_url)
            except Exception as e:
                print(f"  Failed to fetch {current_url}: {e}")
                return

            data = extract_page_data(html, current_url)
            async with self.lock:
                self.page_data[normalized] = data

        # Spawn children after releasing the semaphore so parents don't
        # hold a slot while waiting on their children.
        tasks = []
        for link in data["outgoing_links"]:
            task = asyncio.create_task(self.crawl_page(link))
            self.all_tasks.add(task)
            tasks.append(task)

        try:
            await asyncio.gather(*tasks)
        finally:
            for task in tasks:
                self.all_tasks.discard(task)

    async def crawl(self):
        await self.crawl_page(self.base_url)
        return self.page_data


async def crawl_site_async(base_url, max_concurrency, max_pages):
    async with AsyncCrawler(base_url, max_concurrency, max_pages) as crawler:
        return await crawler.crawl()
