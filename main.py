from aiogram import Bot, Dispatcher
import asyncio
from config.config import load_config
from keyboards.main_menu import set_main_menu
from handlers import user_handlers


async def main():
    bot: Bot = Bot(token=load_config().tg_bot.token, parse_mode='HTML')
    dp: Dispatcher = Dispatcher()
    await set_main_menu(bot)

    dp.include_router(user_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

