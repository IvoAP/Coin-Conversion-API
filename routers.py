from fastapi import APIRouter

router = APIRouter()

@router.get('/convert/ {from_currency}')
def convert(from_currency: str, to_currencies: str, price: float):
    return {"message": "Convert endpoint"}