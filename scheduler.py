import time
import threading
from apscheduler.schedulers.background import BackgroundScheduler
from config import (
    POLL_INSTANTANEOUS_SEC, POLL_EVENTS_SEC, 
    POLL_BILLING_SEC, POLL_LOAD_SURVEY_SEC
)
from meter_reader import MeterReader
from services.polling_service import PollingService
from utils.logger import logger
from database import SessionLocal, init_db
from models import MeterMaster

class SmartMeterScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.reader = MeterReader()
        self.polling_service = PollingService(self.reader)
        self.meter_id = None

    def _ensure_active_meter(self):
        db = SessionLocal()
        try:
            meter = db.query(MeterMaster).first()
            if not meter:
                logger.info("No meter found in database. Creating default simulation meter.")
                meter = MeterMaster(
                    serial_number="SIM-001-2024",
                    manufacturer="SimuTech",
                    location="Lab 1"
                )
                db.add(meter)
                db.commit()
                db.refresh(meter)
            self.meter_id = meter.meter_id
        finally:
            db.close()

    def start(self):
        # Initialize DB and ensure we have a meter ID
        init_db()
        self._ensure_active_meter()
        
        # Connect to meter once at start (or inside jobs if preferred)
        self.reader.dlms_service.connect()

        # Instantaneous Polling
        self.scheduler.add_job(
            self.polling_service.poll_instantaneous,
            'interval',
            seconds=POLL_INSTANTANEOUS_SEC,
            args=[self.meter_id],
            id='poll_instantaneous'
        )

        # Event Polling
        self.scheduler.add_job(
            self.polling_service.poll_events,
            'interval',
            seconds=POLL_EVENTS_SEC,
            args=[self.meter_id],
            id='poll_events'
        )

        # Billing Polling
        self.scheduler.add_job(
            self.polling_service.poll_billing,
            'interval',
            seconds=POLL_BILLING_SEC,
            args=[self.meter_id],
            id='poll_billing'
        )

        # Load Survey Polling
        self.scheduler.add_job(
            self.polling_service.poll_load_survey,
            'interval',
            seconds=POLL_LOAD_SURVEY_SEC,
            args=[self.meter_id],
            id='poll_load_survey'
        )

        self.scheduler.start()
        logger.info("Scheduler started successfully.")

    def stop(self):
        self.scheduler.shutdown()
        self.reader.dlms_service.disconnect()
        logger.info("Scheduler stopped.")

# Global instance
smart_scheduler = SmartMeterScheduler()
