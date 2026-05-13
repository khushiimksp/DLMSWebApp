import streamlit as st
import pandas as pd
import time
from database import SessionLocal
from models import InstantaneousReading, MeterMaster
from config import DASHBOARD_REFRESH_SEC, MAX_CHART_POINTS
import plotly.express as px

def render_live_dashboard():
    st.subheader("📡 Real-Time Meter Monitoring")

    db = SessionLocal()
    try:
        meter = db.query(MeterMaster).first()
        if not meter:
            st.error("No meter connected. Please check database.")
            return

        # Fetch latest reading
        latest = db.query(InstantaneousReading).filter(
            InstantaneousReading.meter_id == meter.meter_id
        ).order_by(InstantaneousReading.timestamp.desc()).first()

        if not latest:
            st.warning("Waiting for first data point...")
            return

        # KPI Metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Voltage R", f"{latest.voltage_r:.2f} V")
        col2.metric("Current R", f"{latest.current_r:.2f} A")
        col3.metric("Frequency", f"{latest.frequency:.2f} Hz")
        col4.metric("Power Factor R", f"{latest.power_factor_r:.3f}")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Active Power", f"{latest.active_power_import:.2f} kW")
        col2.metric("Reactive Power", f"{latest.reactive_power:.2f} kVAR")
        col3.metric("Apparent Power", f"{latest.apparent_power:.2f} kVA")
        col4.metric("Total Energy", f"{latest.active_energy_import:.2f} kWh")

        st.divider()

        # Real-time charts
        history_df = pd.read_sql(
            db.query(InstantaneousReading).filter(
                InstantaneousReading.meter_id == meter.meter_id
            ).order_by(InstantaneousReading.timestamp.desc()).limit(MAX_CHART_POINTS).statement,
            db.bind
        )
        history_df = history_df.sort_values('timestamp')

        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.write("### Voltage Trend (V)")
            fig_v = px.line(history_df, x='timestamp', y=['voltage_r', 'voltage_y', 'voltage_b'],
                           labels={'value': 'Voltage (V)', 'timestamp': 'Time'})
            st.plotly_chart(fig_v, use_container_width=True)

        with chart_col2:
            st.write("### Current Trend (A)")
            fig_i = px.line(history_df, x='timestamp', y=['current_r', 'current_y', 'current_b'],
                           labels={'value': 'Current (A)', 'timestamp': 'Time'})
            st.plotly_chart(fig_i, use_container_width=True)

        # Raw Data Table
        with st.expander("Latest Readings Data Table"):
            st.dataframe(history_df.tail(10))

    finally:
        db.close()
