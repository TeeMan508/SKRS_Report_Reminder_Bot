import sys
from enum import Enum

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import BotCommand
from config import settings

from bot.handlers.command.router import router as command_router
from bot.handlers.callback.router import router as callback_router
from .logger import logger
from .storage.redis import redis_storage


class RunningMode(str, Enum):
    LONG_POLLING = "LONG_POLLING"
    WEBHOOK = "WEBHOOK"


if not settings.BOT_TOKEN:
    logger.error("`TELEGRAM_API_TOKEN` is not set")
    sys.exit(1)

RUNNING_MODE = RunningMode.LONG_POLLING
bot = Bot(token=settings.BOT_TOKEN)

dispatcher = Dispatcher(storage=RedisStorage(redis=redis_storage))
dispatcher.include_router(command_router)
dispatcher.include_router(callback_router)


async def set_bot_commands() -> None:
    await bot.set_my_commands(
        [
            BotCommand(command="/register", description="Register in the bot"),
            BotCommand(command="/id", description="Get the user and chat ids"),
            BotCommand(command="/subscribe", description="Subscribe to notifications"),
            BotCommand(command="/unsubscribe", description="Unsubscribe from notifications"),
        ],
    )


@dispatcher.startup()
async def on_startup() -> None:
    await set_bot_commands()