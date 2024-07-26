from functools import cache
from os import environ, path

from loguru import logger
from pydantic import BaseModel, Field


class LLMDeploymentConfig(BaseModel):
    deployment_id: str = Field(
        default_factory=lambda: environ.get("OPENAI_DEPLOYMENT", "")
    )
    model: str = Field(
        default_factory=lambda: environ.get("OPENAI_MODEL", "gpt-3.5-turbo")
    )


class LLMConfig(BaseModel):
    openai_api_base: str = Field(
        default_factory=lambda: environ.get(
            "AZURE_OPENAI_ENDPOINT",
            environ.get("OPENAI_API_BASE", "https://api.openai.com"),
        ),
    )
    openai_api_key: str = Field(
        default_factory=lambda: environ.get("OPENAI_API_KEY", "")
    )
    openai_api_version: str = Field(
        default_factory=lambda: environ.get("OPENAI_API_VERSION", "2023-07-01-preview")
    )

    reasoning: LLMDeploymentConfig = Field(default_factory=LLMDeploymentConfig)
    retrieval: LLMDeploymentConfig = Field(default_factory=LLMDeploymentConfig)
    embeeding: LLMDeploymentConfig = Field(default_factory=LLMDeploymentConfig)


class AppConfig(BaseModel):
    llm: LLMConfig = Field(default_factory=LLMConfig)


def generate_config(rcfile: str) -> None:
    logger.warning("Generating config file.")
    config = AppConfig()
    with open(rcfile, "w") as fd:
        print(config.model_dump_json(indent=4), file=fd)


@cache
def load_config(cfg_file: str = "", gen_cfg: bool = False) -> AppConfig:
    rcfile = cfg_file if cfg_file else path.join(path.expanduser("~"), ".xxy_cfg.json")
    if not path.exists(rcfile) or gen_cfg:
        generate_config(rcfile)

    with open(rcfile, "r") as fd:
        content = fd.read().strip()
        config = AppConfig.model_validate_json(content)
    new_content = config.model_dump_json(indent=4)
    if content != new_content:
        logger.warning("Updating config file.")
        with open(rcfile, "w") as fd:
            print(new_content, file=fd)

    return config
