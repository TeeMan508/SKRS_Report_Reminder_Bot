from uuid import uuid4

from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from sqlalchemy.exc import IntegrityError

from .router import router
from ...logger import logger, correlation_id_ctx
from ...messages import YOU_ARE_REGISTERED_TEXT, NOTIFICATIONS_TIMER_TEXT, ALREADY_REGISTERED_TEXT
from ...storage.db import async_session
from ...storage.models import User
from ...utils.error_handling import error_handling


class UserState(StatesGroup):
    active = State()
    inactive = State()

    reporting__progress = State()
    reporting__plans = State()
    reporting__problems = State()


@router.message(Command("register"))
@error_handling
async def handle_register_command(message: Message, state: FSMContext) -> None:
    if message.from_user is None:
        return
    correlation_id_ctx.set(uuid4().__str__())
    logger.info("Session starts")

    async with async_session() as session:
        try:
            session.add(User(uid=str(message.from_user.id), name=message.from_user.username))
            await session.commit()
        except IntegrityError:
            await message.answer(f"{ALREADY_REGISTERED_TEXT} {message.from_user.username}")
            return

    await state.set_state(UserState.active)

    await message.answer(f'{YOU_ARE_REGISTERED_TEXT} {message.from_user.username}! {NOTIFICATIONS_TIMER_TEXT}')



