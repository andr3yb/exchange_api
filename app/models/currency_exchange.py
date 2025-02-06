from sqlalchemy import Column, Integer, String, Numeric, TIMESTAMP, ForeignKey, func
from models.base import Base

class CurrencyExchange(Base):
    __tablename__ = "currency_exchange"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    from_currency = Column(String(3), nullable=False)
    to_currency = Column(String(3), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    exchange_rate = Column(Numeric(12, 6), nullable=False)
    result = Column(Numeric(12, 2), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
