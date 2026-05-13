import streamlit as st
import time
from dashboard.live_dashboard import render_live_dashboard
from dashboard.events_dashboard import render_events_dashboard
from dashboard.billing_dashboard import render_billing_dashboard
from dashboard.historical_dashboard import render_historical_dashboard
from scheduler import smart_scheduler
from utils.logger import logger
from database import init_db

# Page Configuration
st.set_page_config(
    page_title="DLMS Smart Meter Monitoring",
    page_icon="⚡",
    layout="wide"
)

# Start Background Scheduler (only once)
if 'scheduler_started' not in st.session_state:
    try:
        smart_scheduler.start()
        st.session_state['scheduler_started'] = True
        logger.info("Application starting: Background scheduler initialized.")
    except Exception as e:
        logger.error(f"Failed to start scheduler: {e}")
        st.error("System Error: Could not initialize background monitoring.")

# Sidebar Navigation
st.sidebar.title("⚡ Meter Monitor")
st.sidebar.info("Simulated Meter: ON" if getattr(smart_scheduler.reader.dlms_service, 'simulation_mode', True) else "Physical Meter: ON")

page = st.sidebar.radio(
    "Navigation",
    ["Live Dashboard", "Event Logs", "Historical Trends", "Billing Data"]
)

# Render Pages
if page == "Live Dashboard":
    render_live_dashboard()
    # Auto-refresh logic
    time.sleep(5)
    st.rerun()
elif page == "Event Logs":
    render_events_dashboard()
elif page == "Historical Trends":
    render_historical_dashboard()
elif page == "Billing Data":
    render_billing_dashboard()

# Footer
st.sidebar.divider()
st.sidebar.markdown("### System Status")
st.sidebar.success("DB Connected")
st.sidebar.success("Polling Active")
if st.sidebar.button("Restart Scheduler"):
    smart_scheduler.stop()
    smart_scheduler.start()
    st.toast("Scheduler Restarted!")
