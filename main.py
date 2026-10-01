import sys
import asyncio
from crawl import crawl_site_async
from json_report import write_json_report

async def main():
    if len(sys.argv) < 4:
        print("not enough arguments provided")
        sys.exit(1)
    if len(sys.argv) > 4:
        print("too many arguments provided")
        sys.exit(1)

    base_url = sys.argv[1]
    max_concurrency = int(sys.argv[2])
    max_pages = int(sys.argv[3])
    print(f"starting crawl of: {base_url}")
    page_data = await crawl_site_async(
        base_url,
        max_concurrency,
        max_pages,
    )
    write_json_report(page_data)
    print(f"Found {len(page_data)} pages")

if __name__ == "__main__":
    asyncio.run(main())
