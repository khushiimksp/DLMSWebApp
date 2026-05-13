import streamlit as st
import pandas as pd
from database import SessionLocal
from models import BillingRecord
import plotly.express as px

def render_billing_dashboard():
    st.subheader("💰 Billing & Consumption History")

    db = SessionLocal()
    try:
        billing_df = pd.read_sql(db.query(BillingRecord).order_by(BillingRecord.billing_date.desc()).statement, db.bind)

        if billing_df.empty:
            st.info("No billing records found. Historical data is generated monthly.")
            return

        # Bar Chart Units
        st.write("### Monthly Consumption (kWh)")
        fig = px.bar(billing_df, x='billing_date', y='active_energy_import', title="Active Energy Import")
        st.plotly_chart(fig, use_container_width=True)

        st.write("### Maximum Demand Trend (kW)")
        fig_md = px.line(billing_df, x='billing_date', y='maximum_demand')
        st.plotly_chart(fig_md, use_container_width=True)

        st.write("### Detailed Billing History")
        st.dataframe(billing_df)
        
        csv = billing_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", csv, "billing_history.csv", "text/csv")

    finally:
        db.close()
