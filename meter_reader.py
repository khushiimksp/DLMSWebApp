import time
from services.dlms_service import DLMSService
from utils.logger import logger

class MeterReader:
    def __init__(self):
        self.dlms_service = DLMSService()
        self.max_retries = 3
        self.retry_delay = 2

    def __enter__(self):
        if self.dlms_service.connect():
            return self
        raise Exception("Could not connect to meter")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dlms_service.disconnect()

    def read_obis(self, obis_code):
        for attempt in range(self.max_retries):
            try:
                return self.dlms_service.read_obis(obis_code)
            except Exception as e:
                logger.warning(f"Read attempt {attempt+1} failed for {obis_code}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    logger.error(f"Failed to read {obis_code} after {self.max_retries} attempts.")
                    raise e
