from typing import Awaitable, List

from langchain_openai.chat_models.base import BaseChatOpenAI

from xxy.typing import Entity, Query


async def select_entity(
    query: Query, entities: List[Entity], llm: BaseChatOpenAI
) -> Entity:
    raise NotImplementedError()
