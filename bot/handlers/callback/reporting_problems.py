from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import select, desc
from sqlalchemy import update

from bot.exceptions import NoEntityException
from bot.utils.error_handling import error_handling
from bot.handlers.command.register import UserState
from bot.handlers.command.router import router
from bot.messages import FINISH_TEXT
from bot.storage.db import async_session
from bot.storage.models import Report
from bot.utils.form_pretty_report import form_pretty_report
from config import settings

bot_instance = Bot(settings.BOT_TOKEN)

@error_handling
@router.message(UserState.reporting__problems)
async def handle_problems_message(message: Message, state: FSMContext) -> None:
    if message.from_user is None:
        return

    problems = message.text
    uid = str(message.from_user.id)

    async with async_session() as session:
        await session.execute(
            update(Report).
            where(Report.user_uid == uid).
            values(problems=problems)
        )
        await session.commit()

        report_qs = await session.execute(
            select(Report).
            where(Report.user_uid == uid).
            order_by(desc(Report.created_at))
        )

        report = report_qs.first()[0]

        if not report:
            raise NoEntityException

        text = form_pretty_report(message.from_user.username ,report.progress, report.plans, report.problems)
        await bot_instance.send_message(int(settings.GROUP_TG_UID),
                                        **text.as_kwargs(),
                                        message_thread_id=settings.TOPIC_THREAD_ID
                                        )

    await state.set_state(UserState.active)
    await message.answer(FINISH_TEXT)








