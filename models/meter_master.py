from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from database import Base

class MeterMaster(Base):
    __tablename__ = "meter_master"

    meter_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    serial_number = Column(String, unique=True, index=True)
    manufacturer = Column(String)
    location = Column(String)
    installation_date = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
