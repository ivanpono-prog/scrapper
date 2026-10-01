import asyncio
import aiohttp
from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup, Tag

class AsyncCrawler:
    def __init__(self, base_url, max_concurrency=10, max_pages=100):
        self.base_url = base_url
        self.base_domain = urlsplit(base_url).netloc
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

            if normalized_url in self.visited:
                return False

            if len(self.visited) >= self.max_pages:
                self.should_stop = True
                print("Reached maximum number of pages to crawl")
                return False

            self.visited.add(normalized_url)
            return True

    async def get_html(self, url: str) -> str:
        async with self.session.get(url, headers={"User-Agent": "BootCrawler/1.0"}) as response:
            response.raise_for_status()
            content_type = response.headers.get("content-type")
            if not content_type or not content_type.startswith("text/html"):
                raise Exception(f"Expected HTML, got {content_type}")
            return await response.text()

    async def crawl_page(self, current_url):
        if self.should_stop:
            return

        current_domain = urlsplit(current_url).netloc

        if current_domain != self.base_domain:
            return

        normalized_url = normalize_url(current_url)
        is_new = await self.add_page_visit(normalized_url)

        if not is_new:
            return

        async with self.semaphore:
            print(f"crawling: {current_url}")
            html = await self.get_html(current_url)

        data = extract_page_data(html, current_url)

        async with self.lock:
            self.page_data[normalized_url] = data

        tasks = []

        for link in data["outgoing_links"]:
            task = asyncio.create_task(self.crawl_page(link))
            self.all_tasks.add(task)
            task.add_done_callback(self.all_tasks.discard)
            tasks.append(task)

        await asyncio.gather(*tasks)

    async def crawl(self):
        await self.crawl_page(self.base_url)
        return self.page_data

async def crawl_site_async(base_url, max_concurrency, max_pages):
    async with AsyncCrawler(
        base_url,
        max_concurrency,
        max_pages,
    ) as crawler:
        page_data = await crawler.crawl()
        return page_data

def normalize_url(url: str) -> str:
    parsed = urlsplit(url)
    normalized = parsed.netloc + parsed.path
    normalized = normalized.rstrip("/")
    return normalized

def get_heading_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    h1_tag = soup.find("h1")
    h2_tag = soup.find("h2")

    if isinstance(h1_tag, Tag):
        return h1_tag.get_text(strip=True)
    elif isinstance(h2_tag, Tag):
        return h2_tag.get_text(strip=True)
    else:
        return ""

def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    main_tag = soup.find("main")

    if isinstance(main_tag, Tag):
        p_tag = main_tag.find("p")
        if isinstance(p_tag, Tag):
            return p_tag.get_text(strip=True)

    p_tag = soup.find("p")
    if isinstance(p_tag, Tag):
        return p_tag.get_text(strip=True)

    return ""

def get_urls_from_html(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href:
            links.append(urljoin(base_url, href))
    return links

def get_images_from_html(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    images = []
    for img in soup.find_all("img"):
        src = img.get("src")
        if src:
            images.append(urljoin(base_url, src))
    return images

def extract_page_data(html: str, page_url: str):
    return {
        "url": page_url,
        "heading": get_heading_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, page_url),
        "image_urls": get_images_from_html(html, page_url),
    }
