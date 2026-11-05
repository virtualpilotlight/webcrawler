import sys

from get_html import get_html


def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    if len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)

    base_url = sys.argv[1]
    print(f"starting crawl of: {base_url}")

    try:
        html = get_html(base_url)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(html)


if __name__ == "__main__":
    main()
