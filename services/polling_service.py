from datetime import datetime
from database import SessionLocal
from models import InstantaneousReading, Event, BillingRecord, LoadSurvey, MeterMaster
from utils.logger import logger
from obis_mapping import OBIS_MAP

class PollingService:
    def __init__(self, reader):
        self.reader = reader

    def poll_instantaneous(self, meter_id):
        logger.info(f"Polling instantaneous data for meter {meter_id}")
        db = SessionLocal()
        try:
            # Read multiple OBIS codes
            reading_data = {"meter_id": meter_id, "timestamp": datetime.utcnow()}
            
            for obis, info in OBIS_MAP.items():
                if info.get("field") and ("7.0" in obis or "8.0" in obis):
                    try:
                        raw_val = self.reader.read_obis(obis)
                        parsed_val = raw_val * info["scale"]
                        reading_data[info["field"]] = parsed_val
                    except Exception as e:
                        logger.warning(f"Failed to read OBIS {obis}: {e}")

            new_reading = InstantaneousReading(**reading_data)
            db.add(new_reading)
            db.commit()
            logger.info("Instantaneous data stored.")
        except Exception as e:
            logger.error(f"Error in poll_instantaneous: {e}")
            db.rollback()
        finally:
            db.close()

    def poll_events(self, meter_id):
        logger.info(f"Polling events for meter {meter_id}")
        db = SessionLocal()
        try:
            # In simulation mode, check for simulated events
            if hasattr(self.reader, 'dlms_service'):
                sim_event = self.reader.dlms_service.get_simulated_events()
                if sim_event:
                    new_event = Event(
                        meter_id=meter_id,
                        event_type=sim_event["event_type"],
                        event_time=sim_event["timestamp"],
                        status=sim_event["status"],
                        description=sim_event["description"]
                    )
                    db.add(new_event)
                    db.commit()
                    logger.info(f"New event detected: {sim_event['event_type']}")
        except Exception as e:
            logger.error(f"Error in poll_events: {e}")
            db.rollback()
        finally:
            db.close()

    def poll_billing(self, meter_id):
        logger.info(f"Polling billing data for meter {meter_id}")
        # Similar logic to instantaneous but for billing OBIS codes
        pass

    def poll_load_survey(self, meter_id):
        logger.info(f"Polling load survey for meter {meter_id}")
        # Periodic 15min interval data
        pass
