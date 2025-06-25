from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from .router import router


@router.message(Command("thread_id"))
async def handle_thread_id_command(message: Message) -> None:
    if message.from_user is None:
        return

    await message.answer(
        f"Thread Id: <b>{message.message_thread_id}</b>",
        parse_mode=ParseMode.HTML,
    )

