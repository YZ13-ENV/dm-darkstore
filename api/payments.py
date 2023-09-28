from fastapi import APIRouter
from fastapi.responses import JSONResponse
from yookassa import Configuration, Payment
import uuid
import dotenv
import os

router = APIRouter(
    prefix='/payments',
    tags=['Оплата']
)

dotenv.load_dotenv()

Configuration.account_id = os.getenv('PAYMENTS_ID')
Configuration.secret_key = os.getenv('PAYMENTS_SECRET_KEY')



@router.post('/getPayment')
async def getPayment(uid: str):
    payment = Payment.create({
        "amount": {
            "value": "199.00",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://api.darkmaterial.space/payments/confirm"
        },
        "capture": True,
        "description": "Подписка DM+"
    }, uuid.uuid4())
    return JSONResponse(content=payment)