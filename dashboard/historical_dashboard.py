import streamlit as st
import pandas as pd
from database import SessionLocal
from models import LoadSurvey, InstantaneousReading
import plotly.express as px

def render_historical_dashboard():
    st.subheader("📊 Historical Trends & Load Profile")

    # Date Range Selection
    col1, col2 = st.columns(2)
    start_date = col1.date_input("Start Date")
    end_date = col2.date_input("End Date")

    db = SessionLocal()
    try:
        # Load Survey Data (15-min intervals)
        st.write("### Load Profile (15-min Intervals)")
        survey_df = pd.read_sql(db.query(LoadSurvey).order_by(LoadSurvey.timestamp.desc()).limit(100).statement, db.bind)
        
        if not survey_df.empty:
            fig = px.area(survey_df, x='timestamp', y='active_energy', title="Load Curve")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No load survey data available yet.")

        # Historical Instantaneous Data
        st.write("### Average Voltage Trend")
        instant_df = pd.read_sql(
            db.query(InstantaneousReading).order_by(InstantaneousReading.timestamp.desc()).limit(500).statement, 
            db.bind
        )
        
        if not instant_df.empty:
            instant_df['avg_volt'] = (instant_df['voltage_r'] + instant_df['voltage_y'] + instant_df['voltage_b']) / 3
            fig_v = px.line(instant_df, x='timestamp', y='avg_volt', title="Average Phase Voltage")
            st.plotly_chart(fig_v, use_container_width=True)

    finally:
        db.close()
