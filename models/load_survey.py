from sqlalchemy import Column, Integer, BigInteger, Float, DateTime, ForeignKey
from datetime import datetime
from database import Base

class LoadSurvey(Base):
    __tablename__ = "load_survey"

    survey_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    meter_id = Column(Integer, ForeignKey("meter_master.meter_id"))
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    interval_minutes = Column(Integer, default=15)
    
    active_energy = Column(Float)
    reactive_energy = Column(Float)
    average_voltage = Column(Float)
    average_current = Column(Float)
