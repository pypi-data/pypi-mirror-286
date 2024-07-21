import asyncio
import logging
from typing import Callable

from ..metastore.redis import RedisStore
from ..serpapi_client.google.client import GoogleSearch

logger = logging.getLogger(__name__)


class ProductScraper:
    def __init__(
        self,
        serpapi_api_key: str,
        gl: str,
        location: str = None,
        serpapi_tpm: int = 10,
        redis_host: str = "localhost",
        redis_port: int = 6379,
        redis_db: int = 0,
        handler: Callable = None,
    ):
        self.gl = gl
        self.location = location
        self.tpm = serpapi_tpm
        self.handler = handler

        self.google = GoogleSearch(api_key=serpapi_api_key, gl=self.gl, location=self.location, tpm=self.tpm)
        self.store = RedisStore(
            gl=gl, location=location, host=redis_host, port=redis_port, db=redis_db, decode_responses=True
        )

    ################################
    # Scrape Product Page
    ################################
    async def start_product_page_scraping(self, update_interval_day: int = 1, wait_for_sec: float = 60.0):
        logger.info("Start product page scraping.")
        while True:
            update_interval_sec = update_interval_day * 86400.0
            product_ids = await self.store.list_product_pages_to_execute(update_interval_sec=update_interval_sec)
            if not product_ids:
                logger.info(f"All products page have been scraped. Wait for {wait_for_sec} seconds...")
                await asyncio.sleep(wait_for_sec)
                continue

            logger.info(f"{len(product_ids)} products will be scraped.")

            coros = [self.scrape_product_page(product_id=product_id) for product_id in product_ids]
            results = await asyncio.gather(*coros, return_exceptions=True)

            for product_id, result in zip(product_ids, results):
                if isinstance(result, Exception):
                    logger.warning(result)
                    continue
                await self.store.set_product_page_executed_at(product_id)

            # sleep
            await asyncio.sleep(0.1)

    async def scrape_product_page(self, product_id: str):
        # scrape
        logger.info(f"Scrape product page: {product_id}")
        return await self.google.product_page(product_id=product_id)

    ################################
    # Scrape Product Offers
    ################################

    ################################
    # Scrape Product Specs
    ################################

    ################################
    # Scrape Product Reviews
    ################################
    async def start_product_reviews_scraping(self, update_interval_day: int = 1, wait_for_sec: float = 60.0):
        while True:
            update_interval_sec = update_interval_day * 86400.0
            product_ids = await self.store.list_product_reviews_to_execute(update_interval_sec=update_interval_sec)
            if not product_ids:
                logger.info(f"All products reviews have been scraped. Wait for {wait_for_sec} seconds...")
                await asyncio.sleep(wait_for_sec)
                continue

            coros = [self.scrape_product_reviews(product_id=product_id) for product_id in product_ids]
            results = await asyncio.gather(*coros, return_exceptions=True)

            # sleep
            await asyncio.sleep(1.0)

    async def scrape_product_reviews(self, product_id: str):
        # scrape product page
        pages = await self.google.product_reviews(q=product_id)

        # set executed_at
        return await self.store.set_product_reviews_executed_at(product_id)
