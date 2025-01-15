import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from cbrService import getCursOnDate

today = datetime.now().strftime('%Y-%m-%d')
print("Курс валют а сегодня:")
print(getCursOnDate(today))