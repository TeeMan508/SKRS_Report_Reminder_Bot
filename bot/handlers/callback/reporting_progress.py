from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.exc import IntegrityError

from bot.handlers.command.register import UserState
from bot.handlers.command.router import router
from bot.logger import logger

from bot.messages import PLANS_TEXT
from bot.storage.db import async_session
from bot.storage.models import Report
from bot.utils.error_handling import error_handling




@router.message(UserState.reporting__progress)
@error_handling
async def handle_progress_message(message: Message, state: FSMContext) -> None:
    if message.from_user is None:
        return

    progress = message.text
    uid = str(message.from_user.id)
    try:
        async with async_session() as session:
            report = Report(user_uid=uid, progress=progress)
            session.add(report)
            await session.commit()
    except IntegrityError:
        logger.info("123123123")

    await state.set_state(UserState.reporting__plans)
    await message.answer(PLANS_TEXT)
