import asyncio
import logging

from .logger import logger, LOGGING_CONFIG
from .bot import bot, dispatcher
from .storage.db import init_db

async def start_polling():
    logging.config.dictConfig(LOGGING_CONFIG)

    logger.info('Initiating dDB')
    await init_db()

    logger.info('Starting polling')

    # logging.error('Dependencies launched')
    # asyncio.create_task(dispatcher.start_polling(bot, handle_signals=False))
    await dispatcher.start_polling(bot, handle_signals=False)


if __name__ == '__main__':
    asyncio.run(start_polling())


