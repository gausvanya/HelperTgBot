import os
from dataclasses import dataclass

from dotenv import load_dotenv, find_dotenv

__all__ = [
    'get_config',
    'BotConfig',
    'LoggingConfig',
    'Config'
]


@dataclass
class BotConfig:
    token: str


@dataclass
class WikiConfig:
    wiki_api_url: str


@dataclass
class LoggingConfig:
    log_level: str
    log_format: str


@dataclass
class Config:
    bot: BotConfig
    logging: LoggingConfig


def load_from_dotenv_file():
    found_dotenv_path = find_dotenv()
    load_dotenv(found_dotenv_path)


def load_wiki_config():
    load_from_dotenv_file()
    env = os.environ
    wiki_api_url = env['WIKI_API_URL']

    return wiki_api_url


def get_config() -> 'Config':
    load_from_dotenv_file()

    env = os.environ

    bot_token = env['BOT_TOKEN']
    logging_log_level = env['LOGGING_LOG_LEVEL']
    logging_log_format = env['LOGGING_FORMAT']

    return Config(
        bot=BotConfig(
            token=bot_token
        ),
        logging=LoggingConfig(
            log_level=logging_log_level,
            log_format=logging_log_format
        ),
    )
