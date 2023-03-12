import time
import schedule
import asyncio

from aiogram import Router, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from lexicon.lexicon import LEXICON_RU
from services.offers_handling import res_values, process_get_values

process_status: bool = True
router: Router = Router()


job = schedule.every(30).seconds.do(process_get_values)


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON_RU['start'])


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON_RU['help'])


@router.message(Command(commands='beginning'))
async def process_beginning_command(message: Message, bot: Bot):
    global process_status
    process_status = True
    process_get_values()
    while process_status:
        if res_values:
            for title, ref, price in res_values:
                await bot.send_message(chat_id=message.from_user.id, text=f'<b>{title}</b>\n'
                                                                          f'<a href="{ref}">Ссылка</a>\n'
                                                                          f'{price}')
            res_values.clear()
        schedule.run_pending()
        await asyncio.sleep(1)


@router.message(Command(commands='cancel'))
async def process_cancel_command(message: Message):
    global process_status
    process_status = False
    await message.answer(LEXICON_RU['cancel'])
    schedule.cancel_job(job)
