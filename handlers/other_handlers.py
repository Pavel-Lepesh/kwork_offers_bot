from aiogram import Router
from aiogram.types import Message

from lexicon.lexicon import LEXICON_RU


router: Router = Router()


@router.message()
async def process_none(message: Message):
    await message.answer(LEXICON_RU['none'])
