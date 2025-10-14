from fastapi import APIRouter, Path
from convert import sync_converter, async_converter
from typing import Any
from asyncio import gather
from schemas import ConvertInput


router: APIRouter = APIRouter(prefix='/converter')

@router.post('/{from_currency}')
def convert(
        body: ConvertInput,
        from_currency: str = Path(..., min_length=3, max_length=3, description="Currency code (e.g., USD, EUR)", pattern="^[A-Z]{3}$"), 
    ) -> list[Any]:
    result: list[Any] = []
    for currency in body.to_currencies:
        response = sync_converter(
            from_currency = from_currency, 
            to_currency= currency, 
            price = body.price
        )

        result.append(response)

    return result

@router.post('/async/{from_currency}')
async def async_convert(
        body: ConvertInput,
        from_currency: str = Path(..., min_length=3, max_length=3, description="Currency code (e.g., USD, EUR)", pattern="^[A-Z]{3}$"),
    ) -> list[Any]:
    coroutines: list[Any] = []
    for currency in body.to_currencies:
        coro =  async_converter(
            from_currency = from_currency, 
            to_currency= currency, 
            price = body.price
        )

        coroutines.append(coro)

    results = await gather(*coroutines)
    return results