import random
import time
from datetime import datetime
import serial
from gurux_dlms.GXDLMSClient import GXDLMSClient
from gurux_dlms.enums import Authentication, InterfaceType
from gurux_dlms.GXDLMSConfigurableCommand import GXDLMSConfigurableCommand
from gurux_dlms.GXDLMSSettings import GXDLMSSettings
from gurux_dlms.objects.GXDLMSObjectCollection import GXDLMSObjectCollection

from config import (
    SIMULATION_MODE, COM_PORT, BAUD_RATE, 
    INTERFACE_TYPE, CLIENT_ADDRESS, SERVER_ADDRESS, AUTH_PASSWORD,
    METER_IP, METER_PORT
)
from utils.logger import logger
from obis_mapping import OBIS_MAP

class DLMSService:
    def __init__(self):
        self.is_connected = False
        self.simulation_mode = SIMULATION_MODE
        self.energy_accumulator = 0.0
        self.client = GXDLMSClient()
        self.media = None
        
        # Configure Client
        self.client.useLogicalNameReferencing = True
        self.client.interfaceType = InterfaceType.HDLC if INTERFACE_TYPE == "HDLC" else InterfaceType.WRAPPER
        self.client.clientAddress = CLIENT_ADDRESS
        self.client.serverAddress = SERVER_ADDRESS
        self.client.authentication = Authentication.LOW if AUTH_PASSWORD else Authentication.NONE
        self.client.password = AUTH_PASSWORD

    def connect(self):
        if self.simulation_mode:
            logger.info("Connecting in SIMULATION MODE...")
            time.sleep(0.5)
            self.is_connected = True
            return True
        
        try:
            logger.info(f"Initiating connection on {COM_PORT} at {BAUD_RATE} baud...")
            
            # Setup Serial Port
            self.media = serial.Serial(
                port=COM_PORT,
                baudrate=BAUD_RATE,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1
            )

            # DLMS Handshake
            # 1. SNRM (Set Normal Response Mode)
            reply = self._read_data_block(self.client.snrmRequest())
            self.client.parseUAReply(reply)
            
            # 2. AARQ (Application Association Request)
            reply = self._read_data_block(self.client.aarqRequest())
            self.client.parseAAREReply(reply)
            
            logger.info("Association Established Successfully.")
            self.is_connected = True
            return True
            
        except Exception as e:
            logger.error(f"DLMS Connection Error: {e}")
            if self.media:
                self.media.close()
            return False

    def _read_data_block(self, data):
        """Helper to send and receive frames over serial"""
        if not self.media:
            return None
        
        self.media.write(data)
        time.sleep(0.1) # Small delay for hardware response
        
        # Read response
        response = bytearray()
        while True:
            b = self.media.read(1)
            if not b:
                break
            response.extend(b)
            if self.client.isReplyComplete(response):
                break
        return response

    def disconnect(self):
        if self.media and self.media.is_open:
            try:
                self.media.write(self.client.disconnectRequest())
                self.media.close()
            except:
                pass
        self.is_connected = False
        logger.info("Disconnected from meter.")

    def read_obis(self, obis_code):
        if not self.is_connected:
            self.connect()
        
        if self.simulation_mode:
            return self._generate_simulated_value(obis_code)
        
        try:
            # Create DLMS Data object for the OBIS code
            # Note: This is an abstraction. Real Gurux usage typically involves
            # getting the object from the association view first.
            from gurux_dlms.objects.GXDLMSData import GXDLMSData
            obj = GXDLMSData(obis_code)
            
            read_req = self.client.read(obj, 2) # 2 is for 'Value' attribute
            reply = self._read_data_block(read_req)
            val = self.client.updateValue(obj, 2, reply)
            
            return float(val) if val is not None else 0.0
            
        except Exception as e:
            logger.error(f"Error reading OBIS {obis_code}: {e}")
            raise e

    def _generate_simulated_value(self, obis_code):
        # Simulation logic remains same for fallback
        if "32.7" in obis_code or "52.7" in obis_code or "72.7" in obis_code: 
            return random.uniform(225.0, 235.0)
        elif "31.7" in obis_code or "51.7" in obis_code or "71.7" in obis_code: # Currents
            return random.uniform(5.0, 12.0)
        elif "14.7" in obis_code: # Frequency
            return random.uniform(49.8, 50.2)
        elif "33.7" in obis_code or "53.7" in obis_code or "73.7" in obis_code: # PF
            return random.uniform(900, 990)
        elif "1.7" in obis_code: # Power
            return random.uniform(1500, 3000)
        elif "1.8" in obis_code: # Energy
            self.energy_accumulator += random.uniform(0.01, 0.05)
            return 10245.0 + self.energy_accumulator
        return 0.0

    def get_simulated_events(self):
        if random.random() < 0.02:
            event_types = ["MAGNETIC_TAMPER", "COVER_OPEN", "POWER_FAILURE", "REVERSE_CURRENT"]
            return {
                "event_type": random.choice(event_types),
                "timestamp": datetime.utcnow(),
                "status": "ACTIVE",
                "description": "Simulation triggered event"
            }
        return None
