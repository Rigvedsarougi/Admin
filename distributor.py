# distributor.py
import streamlit as st
from database import SessionLocal
from models import SalesRecord

def distributor_dashboard():
    st.title("Distributor Dashboard")
    db = SessionLocal()

    # View assigned sales records
    st.subheader("Assigned Sales Records")
    sales_records = db.query(SalesRecord).filter(SalesRecord.assigned_distributor_id == st.session_state.user.id).all()
    if sales_records:
        for record in sales_records:
            with st.expander(f"Order #{record.id} - {record.outlet_name}"):
                st.write(f"**Date:** {record.date}")
                st.write(f"**Order Value:** {record.order_value}")
                payment_status = st.selectbox("Payment Status", ["pending", "done"], key=f"payment_{record.id}", index=0 if record.payment_status == "pending" else 1)
                delivery_status = st.selectbox("Delivery Status", ["pending", "done"], key=f"delivery_{record.id}", index=0 if record.delivery_status == "pending" else 1)
                remarks = st.text_area("Remarks", value=record.remarks, key=f"remarks_{record.id}")
                if st.button("Update", key=f"update_{record.id}"):
                    record.payment_status = payment_status
                    record.delivery_status = delivery_status
                    record.remarks = remarks
                    db.commit()
                    st.success("Record updated successfully!")
