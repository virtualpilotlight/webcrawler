import asyncio
import sys

from crawl import crawl_site_async
from json_repoty import write_json_report


async def main():
    if len(sys.argv) < 4:
        print("usage: uv run main.py URL max_concurrency max_pages")
        sys.exit(1)
    if len(sys.argv) > 4:
        print("too many arguments provided")
        sys.exit(1)

    base_url = sys.argv[1]
    try:
        max_concurrency = int(sys.argv[2])
        max_pages = int(sys.argv[3])
    except ValueError:
        print("max_concurrency and max_pages must be integers")
        sys.exit(1)
    if max_concurrency < 1 or max_pages < 1:
        print("max_concurrency and max_pages must be at least 1")
        sys.exit(1)

    print(f"starting crawl of: {base_url}")

    try:
        page_data = await crawl_site_async(base_url, max_concurrency, max_pages)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    write_json_report(page_data)
    print(f"\nCrawl complete: found {len(page_data)} pages")
    print("Report written to report.json")


if __name__ == "__main__":
    asyncio.run(main())
