import asyncio
from datetime import datetime
from cbrService import getCursOnDate
from botSericve import runBot

today = datetime.now().strftime('%Y-%m-%d')
print("Курс валют а сегодня:")
print(getCursOnDate(today))

bot_token = "---------"
asyncio.run(runBot(bot_token))