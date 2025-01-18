# БОТ ДЛЯ ОТСЛЕЖИВАНИЯ КУРСА ВАЛЮТ 🤑 $ 💲

Данный телеграмм-бот (https://t.me/CB_currencytracker_bot) создан для получения информации о текущем курсе валют при получении запроса от клиента. А также позволяет задать целевое значение, при достижении которого пользователю придёт уведомление.
Значение курса той или иной валюты бот берёт непосредственно с сайта https://www.cbr.ru/currency_base/daily/. Делая запрос каждый раз, как клиент выбирает соответствующую возможность в телеграмм чате 

## Инструкция по запуску кода (MacOS):

- cd «путь к папке с проектом» - перейти к папке с проектом в консоли

- python -m venv venv    - создание и инициализация папки с виртуальной средой

- source venv/bin/activate  - активация виртуальной среды

- pip install -r requirements.txt – установка зависимостей

- python main.py – запуск программы

## Инструкция по запуску кода (Microsoft):

- cd «путь к папке с проектом» - перейти к папке с проектом в консоли

- python -m venv venv    -  создание и инициализация папки с виртуальной средой

- venv/Scripts/activate  - активация виртуальной среды     

(если не получаестя, то из папки с проектом последовательно выполняем команды: 1) cd venv 2) cd Scripts 3) activate 4) cd.. 5) cd..)

- pip install -r requirements.txt – установка зависимостей

- python main.py – запуск программы

### Токен в файле "config.json" мы не стали указывать из-за публичности странички

### Краткое описание механизма работы

#### Сначала происходит установка библиотек:

- aiogram - библиотека, позволяющей развернуть бота для взаимодействия с телеграмм

- opencv-python - библиотека, позволяющей работать с библиотеками

- numpy - библеотека, добавляющей новые функции работы

- asyncio - библиотека, позволяющая реализовать асинхронные процессы

#### Далее из библиотек импортируем классы:

- Bot, Dispatcher  - необходимые классы для работы бота

- ParseMode  - необходимые классы для работы бота

- MemoryStorage  - необходимые классы для работы бота

- types, F, Router   - необходимые классы для работы бота

- Message   - необходимые классы для работы бота

- Command - необходимые классы для работы бота

- np  - импорт numpy для работы с массивом

#### После того, как мы подготовили все библиотеки и классы, добавляем токен бота

#### Далее добавляем главный обработчик и помещаем в него обработчик "router" 

