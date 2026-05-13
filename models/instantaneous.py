from sqlalchemy import Column, Integer, BigInteger, Float, DateTime, ForeignKey
from datetime import datetime
from database import Base

class InstantaneousReading(Base):
    __tablename__ = "instantaneous_readings"

    reading_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    meter_id = Column(Integer, ForeignKey("meter_master.meter_id"))
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    voltage_r = Column(Float)
    voltage_y = Column(Float)
    voltage_b = Column(Float)
    
    current_r = Column(Float)
    current_y = Column(Float)
    current_b = Column(Float)
    
    frequency = Column(Float)
    
    power_factor_r = Column(Float)
    power_factor_y = Column(Float)
    power_factor_b = Column(Float)
    
    active_power_import = Column(Float)
    active_power_export = Column(Float)
    reactive_power = Column(Float)
    apparent_power = Column(Float)
    
    active_energy_import = Column(Float)
    active_energy_export = Column(Float)
