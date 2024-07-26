from typing import Awaitable, List

from xxy.typing import Entity, Query


class DataSourceBase:
    async def search(self, query: Query) -> List[Entity]:
        raise NotImplementedError()
