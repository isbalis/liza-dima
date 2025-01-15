import asyncio # библиотека, позволяющая реализовать асинхронные процессы
import logging # библиотека для вывода информационных ошибок программы
import io      # input/output (для работы с потоком байтов)
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, filters  # необходимые классы для работы бота
from aiogram.enums.parse_mode import ParseMode  # необходимые классы для работы бота
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage  # необходимые классы для работы бота
from aiogram import types, Router    # необходимые классы для работы бота
from aiogram.types import Message       # необходимые классы для работы бота
from aiogram.filters import Command     # необходимые классы для работы бота
from aiogram.fsm.state import State, StatesGroup
import numpy as np               # импорт numpy для работы с массивом




async def runBot(botToken):
    bot = Bot(
                token=botToken,
                default=DefaultBotProperties(
                    parse_mode=ParseMode.HTML,
                )
        )
    router=Router()
    dp = Dispatcher(storage=MemoryStorage()) #главный обработчик действий и уведомлений
    dp.include_router(router) #добавляем обработчик "router" в главный обработчик

    @router.message(Command("start"))
    async def start_handler(msg: Message, state: FSMContext):
        builder = ReplyKeyboardBuilder()
        
        builder.row(
            types.KeyboardButton(text="USD 🇺🇸"),
            types.KeyboardButton(text="EUR 🇪🇺")
        )
        builder.row(
            types.KeyboardButton(text="HKD 🇭🇰"),
            types.KeyboardButton(text="GBP 🇬🇧")
        )
        builder.row(
            types.KeyboardButton(text="AED 🇦🇪"),
            types.KeyboardButton(text="TRY 🇹🇷")
        )

        user_id = msg.from_user.id  
        save_user_data(user_id, "", globalCurrencyFilename)
        save_user_data(user_id, -1, globalNumsFilename)

        helloText= """Приветствуем вас!\nДанный бот создан для отслеживания актуального курса валют.\nВыберите интересующее вас действие из списка:"""
        await state.set_state(Form.cur)
        await msg.answer(
            helloText,
            reply_markup=builder.as_markup(resize_keyboard=True)
        )

    await bot.delete_webhook(drop_pending_updates=True) # отключаем предыдущее соединение бота с сервером телеграмм
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types()) 