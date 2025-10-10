import requests
from os import getenv
from dotenv import load_dotenv
from fastapi import HTTPException
import aiohttp

load_dotenv(override=True)
API_KEY = getenv('APHAVANTAGE_API_KEY')

def sync_converter(from_currency: str, to_currency: str, price:float):
    url  = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={API_KEY}'
    try:
        response = requests.get(url)
    except Exception as error:
        raise HTTPException(status_code=400, detail=error)
    
    data = response.json()
    if "Realtime Currency Exchange Rate" not in data:
        raise HTTPException(status_code=400, detail=f'Realtime currency exchange rate not found {data}')
    
    exchange_rate = float(data['Realtime Currency Exchange Rate']['5. Exchange Rate'])
    
    converted_price = price * exchange_rate
    return converted_price

async def async_converter(from_currency: str, to_currency: str, price:float):
    url  = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={API_KEY}'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
    except Exception as error:
        raise HTTPException(status_code=400, detail=error)
    
    if "Realtime Currency Exchange Rate" not in data:
        raise HTTPException(status_code=400, detail=f'Realtime currency exchange rate not found {data}')
    
    exchange_rate = float(data['Realtime Currency Exchange Rate']['5. Exchange Rate'])
    
    converted_price = price * exchange_rate
    return converted_price