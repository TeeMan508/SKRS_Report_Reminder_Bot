from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import update

from .register import UserState
from .router import router
from ...messages import YOU_ARE_NOT_REGISTERED_TEXT, \
    ALREADY_SUBSCRIBED_TEXT, SUBSCRIBED_SUCCESSFULLY_TEXT, ALREADY_UNSUBSCRIBED_TEXT, UNSUBSCRIBED_SUCCESSFULLY_TEXT
from ...storage.db import async_session
from ...storage.models import User


@router.message(Command("unsubscribe"))
async def handle_unsubscribe_command(message: Message, state: FSMContext) -> None:
    if message.from_user is None:
        return

    uid = str(message.from_user.id)

    try:
        async with async_session() as session:

            rows = await session.execute(
                select(User).
                where(User.uid == uid)
            )
            if not rows.first():
                raise AttributeError

            if not rows.first().is_subsribed:
                raise TypeError

            await session.execute(
                update(User).
                where(User.uid == uid).
                values(is_subsribed=False)
            )

            await session.commit()

    except (IntegrityError, AttributeError):
        await message.answer(YOU_ARE_NOT_REGISTERED_TEXT)
        return
    except TypeError:
        await message.answer(ALREADY_UNSUBSCRIBED_TEXT)
        return

    await state.set_state(UserState.inactive)
    await message.answer(f'{UNSUBSCRIBED_SUCCESSFULLY_TEXT}')



