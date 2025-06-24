from aiogram import F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import update

from bot.handlers.command.register import UserState
from bot.handlers.command.router import router
from bot.logger import logger
from bot.messages import PROGRESS_TEXT, YOU_ARE_NOT_REGISTERED_TEXT
from bot.storage.db import async_session
from bot.storage.models import Report, User
from bot.utils.error_handling import error_handling



@router.callback_query(F.data == "start_report")
@error_handling
async def start_report(callback_query: CallbackQuery, state: FSMContext) -> None:
    if callback_query.message.from_user is None:
        return

    uid = str(callback_query.from_user.id)

    try:
        async with async_session() as session:

            rows = await session.execute(
                select(User).
                where(User.uid == uid)
            )
            if not rows.first():
                raise AttributeError

            await session.commit()

    except (IntegrityError, AttributeError):
        await callback_query.message.answer(YOU_ARE_NOT_REGISTERED_TEXT)
        return

    await state.set_state(UserState.reporting__progress)

    try:
        await callback_query.message.edit_reply_markup(None)
    except TelegramBadRequest:
        ...

    await callback_query.message.answer(PROGRESS_TEXT)
