import asyncio

from aiogram import Router, Bot
from aiogram.filters import Command, CommandStart, Text, StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hide_link

from lexicon.lexicon import LEXICON_RU, HIGH_CATEGORIES, MID_CATEGORIES, LEXICON_CATEGORIES, LOW_CATEGORIES
from services.offers_handling import process_get_values
from keyboards.categoties_kb import create_categories_kb
from database.database import root_categories, root_offers_set, root_res_values, process_status


router: Router = Router()


class FSMFillForm(StatesGroup):
    start_program = State()
    choose_first = State()
    choose_second = State()
    choose_third = State()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON_RU['start'])


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON_RU['help'])


@router.message(Command(commands='cancel'))
async def process_cancel_command(message: Message, state: FSMContext):
    process_status[message.from_user.id] = False
    root_categories[message.from_user.id].clear()  # очищаем категории пользователя
    await message.answer(LEXICON_RU['cancel'])
    await state.set_state(default_state)


@router.message(Command(commands='beginning'), StateFilter(default_state))
async def process_beginning_command(message: Message, state: FSMContext):  # выбираем первую категорию
    await message.answer(text='<b>Выберите категорию!</b>', reply_markup=create_categories_kb(*HIGH_CATEGORIES))
    await state.set_state(FSMFillForm.choose_first)


@router.callback_query(StateFilter(FSMFillForm.choose_first),
                       Text(text=[*HIGH_CATEGORIES]))
async def process_callback_high(callback: CallbackQuery, state: FSMContext):  # выбираем вторую категорию
    root_categories[callback.from_user.id].append(callback.data)  # добавляем первую категорию пользователя
    await callback.message.edit_text(text=f'<b>{callback.data}</b>\n<i>Теперь выберите подкатегорию.</i>',
                                     reply_markup=create_categories_kb(*LEXICON_CATEGORIES[callback.data].keys(),
                                                                       goback_arrow='↩'))
    await state.set_state(FSMFillForm.choose_second)


@router.callback_query(StateFilter(FSMFillForm.choose_second),
                       Text(text='goback_arrow'))
async def second_goback_arrow(callback: CallbackQuery, state: FSMContext):
    root_categories[callback.from_user.id].clear()  # очищаем категории от первого выбора
    await callback.message.edit_text(text='<b>Выберите категорию!</b>',
                                     reply_markup=create_categories_kb(*HIGH_CATEGORIES))
    await state.set_state(FSMFillForm.choose_first)


@router.callback_query(StateFilter(FSMFillForm.choose_second),
                       Text(text=[*MID_CATEGORIES]))
async def process_callback_mid(callback: CallbackQuery, state: FSMContext):  # выбираем третью категорию
    root_categories[callback.from_user.id].append(callback.data)
    await callback.message.edit_text(text=f'{callback.data}\nОтлично! Теперь выберите что будем искать.',
                                     reply_markup=create_categories_kb(
                                         *LEXICON_CATEGORIES[callback.message.text.split('\n')[0]][callback.data],
                                         goback_arrow='↩'))
    await state.set_state(FSMFillForm.choose_third)


@router.callback_query(StateFilter(FSMFillForm.choose_third),
                       Text(text='goback_arrow'))
async def third_goback_arrow(callback: CallbackQuery, state: FSMContext):
    categories = root_categories[callback.from_user.id]
    del categories[-1]  # удаляем предыдущую категорию
    await callback.message.edit_text(text=f'<b>{categories[-1]}</b>\n<i>Теперь выберите подкатегорию.</i>',
                                     reply_markup=create_categories_kb(*LEXICON_CATEGORIES[categories[-1]].keys(),
                                                                       goback_arrow='↩'))
    await state.set_state(FSMFillForm.choose_second)


@router.callback_query(StateFilter(FSMFillForm.choose_third),
                       Text(text=[*LOW_CATEGORIES]))
async def process_callback_low(callback: CallbackQuery, bot: Bot):
    await bot.send_message(chat_id=callback.from_user.id, text=LEXICON_RU['start_process'])
    categories = root_categories[callback.from_user.id]
    categories.append(callback.data)  # добавляем последнюю категорию
    await callback.message.delete()  # удаляем сообщение с клавиатурой для выбора
    user = callback.from_user.id  # id пользователя
    res_values = root_res_values[user]  # результирующие значения для проверки на актуальность
    process_status[user] = True  # отвечает за процесс проверки результатов парсинга
    await process_get_values(root_offers_set[user], res_values, categories)
    while process_status[user]:
        if res_values:
            for title, ref, price in res_values:
                await bot.send_message(chat_id=callback.from_user.id, text=f'{hide_link(ref)}'
                                                                           f'<b>{title}</b>\n'
                                                                           f'{price}')
            res_values.clear()
        await process_get_values(root_offers_set[user], res_values, categories)
        await asyncio.sleep(15)
