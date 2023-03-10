import time

from aiogram import Router, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

import schedule
from services.offers_handling import set_of_offers, res_values, get_offers


router: Router = Router()


def _process_get_values():
    try:
        get_offers(set_of_offers)
    except Exception as err:
        print(err)
        _process_get_values()


schedule.every(30).seconds.do(_process_get_values)


@router.message(CommandStart())
async def process_command_start(message: Message, bot: Bot):
    while True:
        if res_values:
            for title, ref, price in res_values:
                await bot.send_message(chat_id=message.from_user.id, text=f'{title}\n'
                                                                          f'<a href="{ref}">Ссылка</a>\n'
                                                                          f'{price}')

            res_values.clear()
        schedule.run_pending()






@router.message()
async def echo(message: Message):
    await message.answer('No')


