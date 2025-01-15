#главная программа для запуска
import asyncio
from fileService import load_from_file
from botService import runBot

bot_token = load_from_file("config").get("BOT_TOKEN")
asyncio.run(runBot(bot_token))