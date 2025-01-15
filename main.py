import requests
import xml.etree.ElementTree as ET
from datetime import datetime

def getCursOnDate(date):
    # SOAP request URL
    url = "https://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx"
    
    # structured XML
    payload = f"""<?xml version="1.0" encoding="utf-8"?>
                    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                    <soap:Body>
                        <GetCursOnDate xmlns="http://web.cbr.ru/">
                        <On_date>{date}</On_date>
                        </GetCursOnDate>
                    </soap:Body>
                    </soap:Envelope>"""

    # headers
    headers = {
        'Host': 'www.cbr.ru',
        'Content-Type': 'text/xml; charset=utf-8',
        'SOAPAction': '"http://web.cbr.ru/GetCursOnDate"'
    }
    # POST request
    response = requests.request("POST", url, headers=headers, data=payload)


    if(response.status_code == 200):
        root = ET.fromstring(response.text)
        # Find all currency entries
        ns = {'diffgr': 'urn:schemas-microsoft-com:xml-diffgram-v1'}
        currencies = root.findall(".//diffgr:diffgram/ValuteData/ValuteCursOnDate",ns)

        # Extract data
        parsed_data = []
        for currency in currencies:
            name = currency.find("Vname").text.strip()
            nominal = float(currency.find("Vnom").text)
            rate = float(currency.find("Vcurs").text)
            code = currency.find("VchCode").text

            parsed_data.append({
                "name": name,
                "nominal": nominal,
                "rate": rate,
                "code": code,
            })

            # Print parsed data
            # for entry in parsed_data:
            #     print(f"Currency: {entry['name']}, Code: {entry['code']}, Nominal: {entry['nominal']}, Rate: {entry['rate']}")
        return parsed_data
    
    today = datetime.now().strftime('%Y-%m-%d')
    print("Курс валют а сегодня:")
    print(getCursOnDate(today))