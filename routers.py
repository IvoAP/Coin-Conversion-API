from fastapi import APIRouter

router = APIRouter()

@router.get('/convert')
def convert():
    return {"message": "Convert endpoint"}