from functools import cache
from typing import Any, Awaitable, List, Optional

from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings, ChatOpenAI
from langchain_openai.chat_models.base import BaseChatOpenAI
from langchain_openai.embeddings.base import OpenAIEmbeddings
from loguru import logger

from xxy.config import load_config
from xxy.data_source.base import DataSourceBase
from xxy.selector import select_entity
from xxy.typing import Entity, Query


@cache
def get_ebm() -> OpenAIEmbeddings:
    config = load_config()
    common_openai_params = {
        "temperature": 0,
        "api_key": config.llm.openai_api_key,
        "api_version": config.llm.openai_api_version,
    }
    llm: OpenAIEmbeddings
    if len(config.llm.retrieval.deployment_id) > 0:
        logger.info(f"Using AzureOpenAI {config.llm.retrieval.deployment_id}")
        llm = AzureOpenAIEmbeddings(
            azure_endpoint=config.llm.openai_api_base,
            deployment_name=config.llm.retrieval.deployment_id,
            **common_openai_params,  # type: ignore[arg-type,call-arg]
        )
    else:
        logger.info(f"Using OpenAI {config.llm.retrieval.model}")
        llm = OpenAIEmbeddings(
            base_url=config.llm.openai_api_base,
            model=config.llm.retrieval.model,
            **common_openai_params,  # type: ignore[arg-type]
        )
    return llm


@cache
def get_slm() -> BaseChatOpenAI:
    config = load_config()
    common_openai_params = {
        "temperature": 0,
        "api_key": config.llm.openai_api_key,
        "api_version": config.llm.openai_api_version,
    }
    llm: BaseChatOpenAI
    if len(config.llm.retrieval.deployment_id) > 0:
        logger.info(f"Using AzureOpenAI {config.llm.retrieval.deployment_id}")
        llm = AzureChatOpenAI(
            azure_endpoint=config.llm.openai_api_base,
            deployment_name=config.llm.retrieval.deployment_id,
            **common_openai_params,  # type: ignore[arg-type,call-arg]
        )
    else:
        logger.info(f"Using OpenAI {config.llm.retrieval.model}")
        llm = ChatOpenAI(
            base_url=config.llm.openai_api_base,
            model=config.llm.retrieval.model,
            **common_openai_params,  # type: ignore[arg-type]
        )
    return llm


@cache
def get_llm() -> BaseChatOpenAI:
    config = load_config()
    common_openai_params = {
        "temperature": 0,
        "api_key": config.llm.openai_api_key,
        "api_version": config.llm.openai_api_version,
    }
    llm: BaseChatOpenAI
    if len(config.llm.reasoning.deployment_id) > 0:
        logger.info(f"Using AzureOpenAI {config.llm.reasoning.deployment_id}")
        llm = AzureChatOpenAI(
            azure_endpoint=config.llm.openai_api_base,
            deployment_name=config.llm.reasoning.deployment_id,
            **common_openai_params,  # type: ignore[arg-type,call-arg]
        )
    else:
        logger.info(f"Using OpenAI {config.llm.reasoning.model}")
        llm = ChatOpenAI(
            base_url=config.llm.openai_api_base,
            model=config.llm.reasoning.model,
            **common_openai_params,  # type: ignore[arg-type]
        )
    return llm


async def build_table(
    data_source: DataSourceBase, companys: List[str], dates: List[str], names: List[str]
) -> None:
    llm = get_llm()
    for company in companys:
        for date in dates:
            for name in names:
                query = Query(company=company, date=date, entity_name=name)
                candidates = await data_source.search(query)
                print(await select_entity(query, candidates, llm))
