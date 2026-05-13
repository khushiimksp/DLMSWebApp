from sqlalchemy import Column, Integer, BigInteger, String, DateTime, ForeignKey
from datetime import datetime
from database import Base

class Event(Base):
    __tablename__ = "events"

    event_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    meter_id = Column(Integer, ForeignKey("meter_master.meter_id"))
    event_type = Column(String, index=True) # MAGNETIC_TAMPER, COVER_OPEN, etc.
    event_time = Column(DateTime, default=datetime.utcnow, index=True)
    status = Column(String) # ACTIVE / RESTORED
    description = Column(String)
