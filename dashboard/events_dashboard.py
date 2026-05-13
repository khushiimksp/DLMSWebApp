import streamlit as st
import pandas as pd
from database import SessionLocal
from models import Event
import plotly.express as px

def render_events_dashboard():
    st.subheader("⚠️ Tamper & Event Logs")

    db = SessionLocal()
    try:
        events_df = pd.read_sql(db.query(Event).order_by(Event.event_time.desc()).statement, db.bind)

        if events_df.empty:
            st.success("No tamper events detected. System healthy.")
            return

        # Summary Cards
        counts = events_df['event_type'].value_counts()
        cols = st.columns(len(counts))
        for i, (etype, count) in enumerate(counts.items()):
            cols[i % len(counts)].metric(etype, count)

        # Bar Chart
        st.write("### Event Distribution")
        fig = px.bar(events_df['event_type'].value_counts().reset_index(), 
                     x='event_type', y='count', color='event_type')
        st.plotly_chart(fig, use_container_width=True)

        # Filterable Table
        st.write("### All Events")
        st.dataframe(events_df, use_container_width=True)

    finally:
        db.close()
