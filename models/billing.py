from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from datetime import datetime
from database import Base

class BillingRecord(Base):
    __tablename__ = "billing_records"

    billing_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    meter_id = Column(Integer, ForeignKey("meter_master.meter_id"))
    billing_date = Column(DateTime, default=datetime.utcnow)
    
    active_energy_import = Column(Float)
    active_energy_export = Column(Float)
    maximum_demand = Column(Float)
    tariff_1_units = Column(Float)
    tariff_2_units = Column(Float)
