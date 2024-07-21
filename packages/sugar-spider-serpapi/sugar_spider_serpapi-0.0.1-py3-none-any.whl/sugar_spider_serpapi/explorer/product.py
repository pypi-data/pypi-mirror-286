import asyncio
import logging
from typing import Callable

from ..metastore.redis import RedisStore
from ..serpapi_client.google.client import GoogleSearch

logger = logging.getLogger(__name__)


class ProductExplorer:
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
    # Search Products
    ################################
    async def start_product_searching(self, update_interval_day: int = 1, wait_for_sec: float = 60.0):
        logger.info("Start product searching.")
        while True:
            update_interval_sec = update_interval_day * 87600.0
            query_products = await self.store.list_query_products_to_execute(update_interval_sec=update_interval_sec)

            if not query_products:
                logger.info(f"All products have been searched. Wait for {wait_for_sec} seconds...")
                await asyncio.sleep(wait_for_sec)
                continue

            logger.info(f"{len(query_products)} products will be searched.")

            coros = [self.search_and_add_product(product=product) for product in query_products]
            results = await asyncio.gather(*coros, return_exceptions=True)

            for product, result in zip(query_products, results):
                if isinstance(result, Exception):
                    logger.warning(result)
                    continue
                await self.store.set_query_product_executed_at(product)

            # sleep
            await asyncio.sleep(0.1)

    async def search_and_add_product(self, product: str):
        # search
        logger.info(f"Search product: {product}")
        pages = await self.google.shopping(q=product)

        # add
        for page in pages:
            shopping_results = page.get("shopping_results")
            if not shopping_results:
                break
            for item in shopping_results:
                product_id = item.get("product_id")
                if not product_id:
                    # warning here!
                    continue
                _ = await self.store.add_product(item["product_id"])
