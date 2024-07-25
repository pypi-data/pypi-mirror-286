# scraper.py
import asyncio
import aiohttp
import logging
from my_project85.config import BASE_URL

# Get a logger instance for the scraper module
logger = logging.getLogger(__name__)

async def fetch_url(session: aiohttp.ClientSession, endpoint: str):
    url = f"{BASE_URL}{endpoint}"
    logger.info(f"Fetching URL: {url}")
    try:
        async with session.get(url) as response:
            content = await response.text()
            logger.info(f"Successfully fetched {url}")
            logger.debug(f"Content length of {url}: {len(content)} characters")
            return url, content
    except aiohttp.ClientError as e:
        logger.error(f"Failed to fetch {url}: {e}")
        return url, None

async def scrape_urls(urls: list):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        for url, content in results:
            if content:
                logger.info(f"Content retrieved from {url} has {len(content)} characters")
            else:
                logger.warning(f"No content retrieved from {url}")
