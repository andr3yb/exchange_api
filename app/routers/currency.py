from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import timedelta

from schemas.currency import CurrencyConversionRequest, CurrencyConversionResponse, SupportedCurrenciesResponse
from external.external_api import fetch_exchange_rate, fetch_supported_currencies
from dependencies import get_current_user  # Предполагается, что этот dependency уже реализован (JWT-аутентификация)

router = APIRouter()

@router.get("/exchange", response_model=dict)
async def get_exchange_rate(from_currency: str, to_currency: str, current_user: str = Depends(get_current_user)):
    """
    Возвращает курс обмена для валютной пары.
    Пример запроса: GET /currency/exchange?from_currency=USD&to_currency=EUR
    """
    try:
        rate = await fetch_exchange_rate(from_currency, to_currency)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching exchange rate: {str(e)}")
    return {
        "from_currency": from_currency.upper(),
        "to_currency": to_currency.upper(),
        "exchange_rate": rate
    }

@router.post("/convert", response_model=CurrencyConversionResponse)
async def convert_currency(conversion: CurrencyConversionRequest, current_user: str = Depends(get_current_user)):
    """
    Конвертирует заданную сумму из одной валюты в другую.
    """
    try:
        rate = await fetch_exchange_rate(conversion.from_currency, conversion.to_currency)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching exchange rate: {str(e)}")
    
    converted_amount = conversion.amount * rate
    return CurrencyConversionResponse(
        from_currency=conversion.from_currency.upper(),
        to_currency=conversion.to_currency.upper(),
        original_amount=conversion.amount,
        converted_amount=converted_amount,
        exchange_rate=rate
    )

@router.get("/list", response_model=SupportedCurrenciesResponse)
async def list_currencies(current_user: str = Depends(get_current_user)):
    """
    Возвращает список поддерживаемых валют (словарь кодов и курсов относительно базовой валюты).
    """
    try:
        rates = await fetch_supported_currencies()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching currencies: {str(e)}")
    return SupportedCurrenciesResponse(conversion_rates=rates)
