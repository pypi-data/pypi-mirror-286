import asyncio
from datetime import datetime, timedelta
from typing import Union

from redis.asyncio import Redis

from ..common import TZ
from .core import Store

REDIS_NULL = "null"


RK_QUERY_KEYWORD = "query:keyword"
RK_QUERY_PRODUCT = "query:product"
RK_PRODUCT_PAGE = "product:page"
RK_PRODUCT_OFFERS = "product:offers"
RK_PRODUCT_SPECS = "product:specs"
RK_PRODUCT_REVIEWS = "product:reviews"

PRODUCT_RKS = [RK_PRODUCT_PAGE, RK_PRODUCT_OFFERS, RK_PRODUCT_SPECS, RK_PRODUCT_REVIEWS]


class RedisStore:
    def __init__(
        self,
        gl: str,
        location: str = None,
        host="localhost",
        port=6379,
        db=0,
        decode_responses=True,
        protocol=3,
        **kwargs,
    ):
        self.gl = gl.lower()
        self.location = location.lower() if location else REDIS_NULL

        self.redis = Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=decode_responses,
            protocol=protocol,
            **kwargs,
        )

    ################################
    # Common
    ################################
    def _rk_maker(self, topic: str) -> str:
        return f"{topic}:{self.gl}:{self.location}"

    async def _add(self, topic: str, *keys: str) -> list:
        rk = self._rk_maker(topic)
        existing_keys = await self.redis.hkeys(rk)
        async with self.redis.pipeline() as pipe:
            for key in keys:
                if key not in existing_keys:
                    pipe.hset(rk, key, REDIS_NULL)
            return await pipe.execute()

    async def _remove(self, topic: str, *keys: str) -> list:
        rk = self._rk_maker(topic)
        return await self.redis.hdel(rk, *keys)

    async def _set(self, topic: str, *keys: str, datetime_iso: str = None) -> list:
        rk = self._rk_maker(topic)
        # validate
        if datetime_iso not in [None, REDIS_NULL]:
            _ = datetime.fromisoformat(datetime_iso)
        value = datetime_iso if datetime_iso else datetime.now(tz=TZ).isoformat()
        async with self.redis.pipeline() as pipe:
            for key in keys:
                pipe.hset(rk, key, value)
            return await pipe.execute()

    async def _reset(self, topic: str, *keys: str) -> list:
        rk = self._rk_maker(topic)
        keys = await self.redis.hkeys(rk) if not keys else keys
        async with self.redis.pipeline() as pipe:
            for key in keys:
                pipe.hset(rk, key, REDIS_NULL)
            return await pipe.execute()

    async def _list_executed_at(self, topic: str) -> dict:
        rk = self._rk_maker(topic)
        return await self.redis.hgetall(rk)

    async def _list(self, topic: str) -> list:
        rk = self._rk_maker(topic)
        return await self.redis.hkeys(rk)

    async def _list_to_execute(self, topic: str, update_interval_sec: float) -> list:
        rk = self._rk_maker(topic)
        keys = await self.redis.hgetall(rk)
        return self._filter_expired(keys, update_interval_sec=update_interval_sec)

    @staticmethod
    def _filter_expired(value: dict, update_interval_sec: int) -> list:
        expired_at = datetime.now(tz=TZ) - timedelta(seconds=update_interval_sec)
        expired = list()
        for k, updated_at in value.items():
            if updated_at == REDIS_NULL:
                expired.append(k)
                continue
            if datetime.fromisoformat(updated_at) < expired_at:
                expired.append(k)
        return expired

    ################################
    # Query Keywords
    ################################
    # add
    async def add_query_keyword(self, *queries: str) -> list:
        return await self._add(RK_QUERY_KEYWORD, *queries)

    # remove
    async def remove_query_keyword(self, *queries: str) -> list:
        return await self._remove(RK_QUERY_KEYWORD, *queries)

    # set
    async def set_query_keyword_executed_at(self, *queries: str, datetime_iso: str = None) -> list:
        return await self._set(RK_QUERY_KEYWORD, *queries, datetime_iso=datetime_iso)

    # reset
    async def reset_query_keyword_executed_at(self, *queries: str) -> list:
        return await self._reset(RK_QUERY_KEYWORD, *queries)

    # list
    async def list_query_keywords_executed_at(self) -> dict:
        return await self._list_executed_at(RK_QUERY_KEYWORD)

    async def list_query_keywords(self) -> list:
        return await self._list(RK_QUERY_KEYWORD)

    async def list_query_keywords_to_execute(self, update_interval_sec: int = 86400) -> list:
        return await self._list_to_execute(RK_QUERY_KEYWORD, update_interval_sec=update_interval_sec)

    ################################
    # Query Products
    ################################
    # add
    async def add_query_product(self, *products: str) -> list:
        return await self._add(RK_QUERY_PRODUCT, *products)

    # remove
    async def remove_query_product(self, *products: str) -> list:
        return await self._remove(RK_QUERY_PRODUCT, *products)

    # set
    async def set_query_product_executed_at(self, *products: str, datetime_iso: str = None) -> list:
        return await self._set(RK_QUERY_PRODUCT, *products, datetime_iso=datetime_iso)

    # reset
    async def reset_query_product_executed_at(self, *products: str) -> list:
        return await self._reset(RK_QUERY_PRODUCT, *products)

    # list
    async def list_query_products_executed_at(self) -> dict:
        return await self._list_executed_at(RK_QUERY_PRODUCT)

    async def list_query_products(self) -> list:
        return await self._list(RK_QUERY_PRODUCT)

    async def list_query_products_to_execute(self, update_interval_sec: int = 86400) -> list:
        return await self._list_to_execute(RK_QUERY_PRODUCT, update_interval_sec=update_interval_sec)

    ################################
    # Product
    ################################
    # add
    async def add_product(self, *product_ids: str):
        coros = [self._add(topic, *product_ids) for topic in PRODUCT_RKS]
        return await asyncio.gather(*coros)

    # remove
    async def remove_product(self, *product_ids: str):
        coros = [self._remove(topic, *product_ids) for topic in PRODUCT_RKS]
        return await asyncio.gather(*coros)

    ################################
    # Product Page
    ################################
    # add
    async def add_product_page(self, *product_ids: str):
        return await self._add(RK_PRODUCT_PAGE, *product_ids)

    # remove
    async def remove_product_page(self, *product_ids: str):
        return await self._remove(RK_PRODUCT_PAGE, *product_ids)

    # set
    async def set_product_page_executed_at(self, *product_ids: str, datetime_iso: str = None):
        return await self._set(RK_PRODUCT_PAGE, *product_ids, datetime_iso=datetime_iso)

    # reset
    async def reset_product_page_executed_at(self, *product_ids: str) -> list:
        return await self._reset(RK_PRODUCT_PAGE, *product_ids)

    # list
    async def list_product_pages_executed_at(self) -> dict:
        return await self._list_executed_at(RK_PRODUCT_PAGE)

    async def list_product_pages(self) -> list:
        return await self._list(RK_PRODUCT_PAGE)

    async def list_product_pages_to_execute(self, update_interval_sec: int = 86400 * 7) -> list:
        return await self._list_to_execute(RK_PRODUCT_PAGE, update_interval_sec=update_interval_sec)

    ################################
    # Product Offers
    ################################
    # add
    async def add_product_offers(self, *product_ids: str):
        return await self._add(RK_PRODUCT_OFFERS, *product_ids)

    # remove
    async def remove_product_offers(self, *product_ids: str):
        return await self._remove(RK_PRODUCT_OFFERS, *product_ids)

    # set
    async def set_product_offers_executed_at(self, *product_ids: str, datetime_iso: str = None):
        return await self._set(RK_PRODUCT_OFFERS, *product_ids, datetime_iso=datetime_iso)

    # reset
    async def reset_product_offers_executed_at(self, *product_ids: str) -> list:
        return await self._reset(RK_PRODUCT_OFFERS, *product_ids)

    # list
    async def list_product_offers_executed_at(self) -> dict:
        return await self._list_executed_at(RK_PRODUCT_OFFERS)

    async def list_product_offers(self) -> list:
        return await self._list(RK_PRODUCT_OFFERS)

    async def list_product_offers_to_execute(self, update_interval_sec: int = 86400) -> list:
        return await self._list_to_execute(RK_PRODUCT_OFFERS, update_interval_sec=update_interval_sec)

    ################################
    # Product Specs
    ################################
    # add
    async def add_product_specs(self, *product_ids: str):
        return await self._add(RK_PRODUCT_SPECS, *product_ids)

    # remove
    async def remove_product_specs(self, *product_ids: str):
        return await self._remove(RK_PRODUCT_SPECS, *product_ids)

    # set
    async def set_product_specs_executed_at(self, *product_ids: str, datetime_iso: str = None):
        return await self._set(RK_PRODUCT_SPECS, *product_ids, datetime_iso=datetime_iso)

    # reset
    async def reset_product_specs_executed_at(self, *product_ids: str) -> list:
        return await self._reset(RK_PRODUCT_SPECS, *product_ids)

    # list
    async def list_product_specs_executed_at(self) -> dict:
        return await self._list_executed_at(RK_PRODUCT_SPECS)

    async def list_product_specs(self) -> list:
        return await self._list(RK_PRODUCT_SPECS)

    async def list_product_specs_to_execute(self, update_interval_sec: int = 86400 * 7) -> list:
        return await self._list_to_execute(RK_PRODUCT_SPECS, update_interval_sec=update_interval_sec)

    ################################
    # Product Reviews
    ################################
    # add
    async def add_product_reviews(self, *product_ids: str):
        return await self._add(RK_PRODUCT_REVIEWS, *product_ids)

    # remove
    async def remove_product_reviews(self, *product_ids: str):
        return await self._remove(RK_PRODUCT_REVIEWS, *product_ids)

    # set
    async def set_product_reviews_executed_at(self, *product_ids: str, datetime_iso: str = None):
        return await self._set(RK_PRODUCT_REVIEWS, *product_ids, datetime_iso=datetime_iso)

    # reset
    async def reset_product_reviews_executed_at(self, *product_ids: str) -> list:
        return await self._reset(RK_PRODUCT_REVIEWS, *product_ids)

    # list
    async def list_product_reviews_executed_at(self) -> dict:
        return await self._list_executed_at(RK_PRODUCT_REVIEWS)

    async def list_product_reviews(self) -> list:
        return await self._list(RK_PRODUCT_REVIEWS)

    async def list_product_reviews_to_execute(self, update_interval_sec: int = 86400) -> list:
        return await self._list_to_execute(RK_PRODUCT_REVIEWS, update_interval_sec=update_interval_sec)
