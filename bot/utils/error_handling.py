from functools import wraps

from aiogram import Bot

from ..logger import logger
from ..messages import EXCEPTION_TEXT
from config import settings

bot_instance = Bot(settings.BOT_TOKEN)


def error_handling(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            await func(*args, **kwargs)
        except Exception as e: # noqa
            logger.info(e)
            try:
                await args[0].answer(EXCEPTION_TEXT)
                await bot_instance.send_message(
                    int(settings.ADMIN_TG_UID),
                    f"Smth wrong with bot:\n"
                    f"User: {args[0].from_user.username}\n"
                    f"Handler: {func.__name__}"
                    f"Exception: {e.__str__()}"
                )

            except AttributeError:
                await args[0].message.answer(EXCEPTION_TEXT)
                await bot_instance.send_message(
                    int(settings.ADMIN_TG_UID),
                    f"Smth wrong with bot:\n"
                    f"User: {args[0].message.from_user.username}\n"
                    f"Handler: {func.__name__}\n"
                    f"Exception: {e.__str__()}"
                )

    return wrapper

