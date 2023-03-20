from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_categories_kb(*args, **kwargs) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = [InlineKeyboardButton(text=button, callback_data=button) for button in args]
    kb_builder.row(*buttons, width=1)
    if kwargs:
        kb_builder.row(*[InlineKeyboardButton(text=text, callback_data=callback) for callback, text in kwargs.items()],
                       width=2)
    return kb_builder.as_markup()
