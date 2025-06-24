from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message


from .router import router
from ...logger import logger
from ...messages import YOU_ARE_REGISTERED_TEXT, NOTIFICATIONS_TIMER_TEXT
from ...storage.db import async_session
from ...storage.models import User

class UserState(StatesGroup):
    active = State()
    inactive = State()

    reporting__progress = State()
    reporting__plans = State()
    reporting__problems = State()


@router.message(Command("register"))
async def handle_register_command(message: Message, state: FSMContext) -> None:
    if message.from_user is None:
        return

    logger.info("Session starts")

    async with async_session() as session:
        session.add(User(uid=str(message.from_user.id), name=message.from_user.username))
        await session.commit()

    await state.set_state(UserState.active)

    await message.answer(f'{YOU_ARE_REGISTERED_TEXT} {message.from_user.username}! {NOTIFICATIONS_TIMER_TEXT}')



