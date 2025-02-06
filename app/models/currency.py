from sqlalchemy import Column, String
from models.base import Base

class Currency(Base):
    __tablename__ = "currencies"

    code = Column(String(3), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
