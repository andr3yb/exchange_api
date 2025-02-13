from pydantic import BaseModel
from typing import Dict

class CurrencyConversionRequest(BaseModel):
    from_currency: str
    to_currency: str
    amount: float = 1.0

class CurrencyConversionResponse(BaseModel):
    from_currency: str
    to_currency: str
    original_amount: float
    converted_amount: float
    exchange_rate: float

class SupportedCurrenciesResponse(BaseModel):
    conversion_rates: Dict[str, float]
