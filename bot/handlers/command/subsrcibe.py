from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import update

from .register import UserState
from .router import router
from ...exceptions import NoEntityException, SameStateException
from ...logger import logger
from ...messages import YOU_ARE_NOT_REGISTERED_TEXT, \
    ALREADY_SUBSCRIBED_TEXT, SUBSCRIBED_SUCCESSFULLY_TEXT
from ...storage.db import async_session
from ...storage.models import User
from ...utils.error_handling import error_handling


@router.message(Command("subscribe"))
@error_handling
async def handle_subscribe_command(message: Message, state: FSMContext) -> None:
    if message.from_user is None:
        return

    uid = str(message.from_user.id)

    try:
        async with async_session() as session:
            rows = await session.execute(
                select(User).
                where(User.uid == uid)
            )
            obj = rows.first()[0]

            if not obj:
                raise NoEntityException

            if obj.is_subscribed:
                raise SameStateException

            await session.execute(
                update(User).
                where(User.uid == uid).
                values(is_subscribed=True)
            )

            await session.commit()

    except (IntegrityError, NoEntityException):
        await message.answer(YOU_ARE_NOT_REGISTERED_TEXT)
        return
    except SameStateException:
        await message.answer(ALREADY_SUBSCRIBED_TEXT)
        return

    await state.set_state(UserState.active)
    await message.answer(f'{SUBSCRIBED_SUCCESSFULLY_TEXT}')



