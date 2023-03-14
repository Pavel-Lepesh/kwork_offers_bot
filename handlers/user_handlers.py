import schedule
import asyncio

from aiogram import Router, Bot
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message, CallbackQuery

from lexicon.lexicon import LEXICON_RU, HIGH_CATEGORIES, MID_CATEGORIES, LEXICON_CATEGORIES, LOW_CATEGORIES
from services.offers_handling import res_values, process_get_values, categories
from keyboards.categoties_kb import create_categories_kb

process_status: bool = True
router: Router = Router()


job = schedule.every(30).seconds.do(process_get_values)


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON_RU['start'])


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON_RU['help'])


@router.message(Command(commands='cancel'))
async def process_cancel_command(message: Message):
    global process_status
    process_status = False
    await message.answer(LEXICON_RU['cancel'])
    schedule.cancel_job(job)


@router.message(Command(commands='beginning'))
async def process_beginning_command(message: Message, categories=categories):
    categories = []
    await message.answer(text='<b>Выберите категорию!</b>', reply_markup=create_categories_kb(*HIGH_CATEGORIES))


@router.callback_query(Text(text=[*HIGH_CATEGORIES]))
async def process_callback_high(callback: CallbackQuery):
    categories.append(callback.data)
    await callback.message.edit_text(text=f'<b>{callback.data}</b>\n<i>Теперь выберите подкатегорию.</i>',
                                     reply_markup=create_categories_kb(*LEXICON_CATEGORIES[callback.data].keys()))


@router.callback_query(Text(text=[*MID_CATEGORIES]))
async def process_callback_mid(callback: CallbackQuery):
    categories.append(callback.data)
    await callback.message.edit_text(text=f'{callback.data}\nОтлично! Теперь выберите что будем искать.',
                                     reply_markup=create_categories_kb(*LEXICON_CATEGORIES[callback.message.text.split('\n')[0]][callback.data]))


@router.callback_query(Text(text=[*LOW_CATEGORIES]))
async def process_callback_low(callback: CallbackQuery, bot: Bot):
    categories.append(callback.data)
    await callback.message.delete()
    global process_status
    process_status = True
    process_get_values()
    while process_status:
        if res_values:
            for title, ref, price in res_values:
                await bot.send_message(chat_id=callback.from_user.id, text=f'<b>{title}</b>\n'
                                                                          f'<a href="{ref}">Ссылка</a>\n'
                                                                          f'{price}')
            res_values.clear()
        schedule.run_pending()
        print(1)
        await asyncio.sleep(1)



