import asyncio
import os

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select

from bot.messages import REPORT_NOTIFICATION_TEXT
from bot.bot import bot
from bot.storage.db import async_session
from bot.storage.models import User


if not os.environ.get("LOCAL_DB_ENABLED"):
    os.environ["LOCAL_DB_ENABLED"] = "1"

async def ask_for_report() -> None:
    subscribed_users_ids: list[str] = []
    async with async_session() as session:
        rows = await session.execute(
            select(User).
            where(User.is_subscribed == True)
        )

        if not rows.first():
            print("No users subscribed!")
            return

        for row in rows.all():
            usr_id = row[0].uid
            subscribed_users_ids.append(usr_id)

    for user_id in subscribed_users_ids:
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(text="Начать отчет", callback_data="start_report"))

        await bot.send_message(int(user_id), REPORT_NOTIFICATION_TEXT,  reply_markup=builder.as_markup())

asyncio.run(ask_for_report())