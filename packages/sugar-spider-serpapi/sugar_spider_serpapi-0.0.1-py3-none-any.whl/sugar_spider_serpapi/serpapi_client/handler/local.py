import asyncio
from typing import Callable

from .parser import google_search_parser


class LocalStore:
    def __init__(self, parser: Callable = google_search_parser):
        self.parser = parser
        self.store = list()

    async def __call__(self, *pages: dict):
        for page in pages:
            records = self.parser(page=page)
            self.store += records
