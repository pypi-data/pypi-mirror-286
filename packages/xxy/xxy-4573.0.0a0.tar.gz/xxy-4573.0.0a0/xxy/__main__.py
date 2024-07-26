import argparse
import asyncio
import logging
import sys

from loguru import logger

from xxy.__about__ import __version__
from xxy.agent import build_table
from xxy.config import load_config
from xxy.data_source.folder import FolderDataSource


async def amain() -> None:
    parser = argparse.ArgumentParser(description="xxy-" + __version__)
    parser.add_argument("-v", action="count", default=0, help="verbose level.")
    parser.add_argument(
        "-c",
        default="",
        help="Configuration file path. if not provided, use `~/.xxy_cfg.json` .",
    )
    parser.add_argument(
        "--gen_cfg",
        action="store_true",
        help="Regenerate config from environment variables.",
    )
    args = parser.parse_args()

    logger.remove()
    log_format = "{message}"
    if args.v >= 4:
        logger.add(sys.stderr, level="TRACE", format=log_format)
    elif args.v >= 3:
        logger.add(sys.stderr, level="DEBUG", format=log_format)
    elif args.v >= 2:
        logger.add(sys.stderr, level="INFO", format=log_format)
    elif args.v >= 1:
        logger.add(sys.stderr, level="SUCCESS", format=log_format)
    else:
        logger.add(sys.stderr, level="WARNING", format=log_format)

    if args.v < 4:
        # avoid "WARNING! deployment_id is not default parameter."
        langchain_logger = logging.getLogger("langchain.chat_models.openai")
        langchain_logger.disabled = True

    config = load_config(gen_cfg=args.gen_cfg)
    data_source = FolderDataSource()
    await build_table(data_source, ["000002.SZ"], ["2023Q1"], ["主营业务收入"])


def main() -> None:
    asyncio.run(amain())


if __name__ == "__main__":
    main()
