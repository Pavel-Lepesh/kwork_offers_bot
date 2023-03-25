from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import Redis, RedisStorage
import asyncio
import logging

from config.config import load_config
from keyboards.main_menu import set_main_menu
from handlers import user_handlers, other_handlers


async def main():
    redis: Redis = Redis(host='localhost')
    storage: RedisStorage = RedisStorage(redis=redis)
    logging.basicConfig(level=logging.INFO)
    bot: Bot = Bot(token=load_config().tg_bot.token, parse_mode='HTML')
    dp: Dispatcher = Dispatcher(storage=storage)
    await set_main_menu(bot)

    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
