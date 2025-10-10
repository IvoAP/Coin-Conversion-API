from fastapi import APIRouter, Query, Path
from convert import sync_converter, async_converter
from typing import Any, Annotated
from asyncio import gather


router = APIRouter()


router = APIRouter(prefix='/converter')

@router.get('/{from_currency}')
def convert(
        from_currency: str = Path(..., min_length=3, max_length=3, description="Currency code (e.g., USD, EUR)", pattern="^[A-Z]{3}$"), 
        price: float = Query(..., gt=0, description="Amount to convert"), 
        to_currencies: list[Annotated[str, Query(min_length=3, max_length=3, pattern="^[A-Z]{3}$")]] = Query(default=['USD'], min_length=1, max_length=5, description="List of target currency codes")
    ) -> list[Any]:
    result: list[Any] = []
    for currency in to_currencies:
        response = sync_converter(
            from_currency = from_currency, 
            to_currency= currency, 
            price = price
        )

        result.append(response)

    return result

@router.get('/async/{from_currency}')
async def async_convert(
        from_currency: str = Path(..., min_length=3, max_length=3, description="Currency code (e.g., USD, EUR)", pattern="^[A-Z]{3}$"),
        price: float = Query(..., gt=0, description="Amount to convert"), 
        to_currencies: list[Annotated[str, Query(min_length=3, max_length=3, pattern="^[A-Z]{3}$")]] = Query(default=['USD'], min_length=1, max_length=5, description="List of target currency codes")
    ) -> list[Any]:
    coroutines: list[Any] = []
    for currency in to_currencies:
        coro =  async_converter(
            from_currency = from_currency, 
            to_currency= currency, 
            price = price
        )

        coroutines.append(coro)

    results = await gather(*coroutines)
    return results