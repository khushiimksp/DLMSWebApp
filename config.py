# Meter Connection
COM_PORT = "COM3"           # Change to actual port
BAUD_RATE = 9600
CLIENT_ADDRESS = 16
SERVER_ADDRESS = 1
AUTH_PASSWORD = "YOUR_METER_PASSWORD"
INTERFACE_TYPE = "HDLC"     # or "WRAPPER" for TCP

# TCP/IP (if using network meter)
METER_IP = "192.168.1.100"
METER_PORT = 4059

# Simulation Mode (Set True to test without physical meter)
SIMULATION_MODE = True

# Database
DATABASE_URL = "sqlite:///smart_meter.db"   # Swap for PostgreSQL/SQL Server URI

# Polling Frequencies (seconds)
POLL_INSTANTANEOUS_SEC = 5
POLL_EVENTS_SEC = 30
POLL_BILLING_SEC = 3600
POLL_LOAD_SURVEY_SEC = 900

# Dashboard
DASHBOARD_REFRESH_SEC = 5
MAX_CHART_POINTS = 200
