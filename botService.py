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
from fileService import save_to_file, load_from_file, save_user_data, load_user_data
from cbrService import getCurrency


async def runBot(botToken):
    globalCurrencyFilename= "userCurrencies"
    globalNumsFilename = "userNums"


    class Form(StatesGroup):
        num = State()
        cur = State()
    
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

    @router.message(Form.cur)
    async def chooseCurrency(message: types.Message, state: FSMContext):
        current_state = await state.get_state()
        if current_state is None:
            return
        if current_state != Form.cur.state:
            return
        try:
            currency = message.text
            await state.clear()
            builder = ReplyKeyboardBuilder()
            builder.row(
            types.KeyboardButton(text="целевое значение"),
                types.KeyboardButton(text="курс валют")
            )
            await state.update_data(selCur = currency)
            user_id = message.from_user.id  
            save_user_data(user_id, currency, globalCurrencyFilename)
            await message.answer(f"Выбрана валюта {currency}. \nТеперь выберите действие:",
            reply_markup=builder.as_markup(resize_keyboard=True))
        except ValueError:
            await message.answer("Вы должны указать валюту из списка! Попробуйте ещё раз.")
        return 

    @router.message(F.text.casefold() == "целевое значение")
    async def enter_num(message: types.Message, state: FSMContext):
        await state.clear()
        await state.set_state(Form.num)
        await message.reply("Задайте целевое значение курса (введите число).")

    @router.message(Form.num)
    async def enterNum(message: types.Message, state: FSMContext):
        try:
            number = int(message.text)
            user_id = message.from_user.id  
            save_user_data(user_id, number, globalNumsFilename)
            user_data = load_user_data(globalCurrencyFilename)
            currency = user_data.get(str(user_id), "??")
            await message.answer(f"Спасибо! Мы уведомим вас, когда значение курса для {currency} будет больше {number}!")
            await state.clear()
        except ValueError:
            await message.answer("Вы должны указать числовое значение! Попробуйте ещё раз.")

    @router.message(F.text.casefold() == "курс валют")
    async def enter_num(message: types.Message, state: FSMContext):
        await state.clear()
        user_id = message.from_user.id
        user_data = load_user_data(globalCurrencyFilename)  
        currency = user_data.get(str(user_id), "??")
        currency = currency.split(" ")[0]
        today = datetime.now().strftime('%Y-%m-%d')
        info = getCurrency(today, currency.upper())
        if info is not None:
            await message.reply(f"Курс {currency} на сегодня:\nКурс: {info['rate']}\nНоминал: {info['nominal']}\nКод: {info['code']}\nПолное название: {info['name']}")
        else:
            await message.reply("Произошла ошибка! Повторите запрос позднее.")
            
    await bot.delete_webhook(drop_pending_updates=True) # отключаем предыдущее соединение бота с сервером телеграмм
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types()) 