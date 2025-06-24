from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import update

from bot.utils.error_handling import error_handling
from bot.handlers.command.register import UserState
from bot.handlers.command.router import router

from bot.messages import BLOCKERS_TEXT
from bot.storage.db import async_session
from bot.storage.models import Report


@router.message(UserState.reporting__plans)
@error_handling
async def handle_plans_message(message: Message, state: FSMContext) -> None:
    if message.from_user is None:
        return

    plans = message.text
    uid = str(message.from_user.id)

    async with async_session() as session:
        await session.execute(
            update(Report).
            where(Report.user_uid == uid).
            values(plans=plans)
        )
        await session.commit()

    await state.set_state(UserState.reporting__problems)
    await message.answer(BLOCKERS_TEXT)








