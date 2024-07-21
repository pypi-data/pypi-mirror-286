from abc import ABC, abstractmethod


class Store(ABC):
    ################################
    # Query
    ################################
    @abstractmethod
    async def add_query(self, *queries: str) -> list:
        pass

    @abstractmethod
    async def delete_query(self, *queries: str) -> list:
        pass

    @abstractmethod
    async def update_query_executed_at(self, *queries: str) -> list:
        pass

    @abstractmethod
    async def reset_query_executed_at(self, *queries: str) -> list:
        pass

    @abstractmethod
    async def list_queries_executed_at(self) -> dict:
        pass

    @abstractmethod
    async def list_queries(self) -> list:
        pass

    @abstractmethod
    async def list_queries_to_execute(self, before_sec: int = 86400) -> list:
        pass

    ################################
    # Product
    ################################
    @abstractmethod
    async def add_product(self, *products: str) -> list:
        pass

    @abstractmethod
    async def delete_product(self, *products: str) -> list:
        pass

    @abstractmethod
    async def update_product_executed_at(self, *products: str) -> list:
        pass

    @abstractmethod
    async def reset_product_updated_at(self, *products: str) -> list:
        pass

    @abstractmethod
    async def list_products_executed_at(self) -> dict:
        pass

    @abstractmethod
    async def list_products(self) -> list:
        pass

    @abstractmethod
    async def list_products_to_execute(self, before_sec: int = 86400) -> list:
        pass
