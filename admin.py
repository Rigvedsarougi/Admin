# admin.py
import streamlit as st
from database import SessionLocal
from models import SalesRecord, User
import pandas as pd
import plotly.express as px

def admin_dashboard():
    st.title("Admin Dashboard")
    db = SessionLocal()

    # Add sales record
    st.subheader("Add Sales Record")
    with st.form("sales_form"):
        date = st.date_input("Date")
        outlet_name = st.text_input("Outlet Name")
        address = st.text_input("Address")
        owner_name = st.text_input("Owner Name")
        contact_number = st.text_input("Contact Number")
        gstin_un = st.text_input("GSTIN/UN")
        products_ordered = st.text_input("Products Ordered")
        quantity = st.number_input("Quantity", min_value=1)
        order_value = st.number_input("Order Value", min_value=0.0)
        assigned_distributor_id = st.selectbox("Assign to Distributor", [user.id for user in db.query(User).filter(User.role == "distributor").all()])
        if st.form_submit_button("Submit"):
            sales_record = SalesRecord(
                date=date,
                outlet_name=outlet_name,
                address=address,
                owner_name=owner_name,
                contact_number=contact_number,
                gstin_un=gstin_un,
                products_ordered=products_ordered,
                quantity=quantity,
                order_value=order_value,
                assigned_distributor_id=assigned_distributor_id
            )
            db.add(sales_record)
            db.commit()
            st.success("Sales record added successfully!")

    # View sales records
    st.subheader("Sales Records")
    sales_records = db.query(SalesRecord).all()
    if sales_records:
        df = pd.DataFrame([{
            "Date": record.date,
            "Outlet Name": record.outlet_name,
            "Order Value": record.order_value,
            "Assigned Distributor": record.assigned_distributor.username,
            "Payment Status": record.payment_status,
            "Delivery Status": record.delivery_status
        } for record in sales_records])
        st.dataframe(df)

        # Sales insights
        st.subheader("Sales Insights")
        fig = px.bar(df, x="Date", y="Order Value", color="Assigned Distributor", title="Sales by Date and Distributor")
        st.plotly_chart(fig)

    # Export sales records
    st.subheader("Export Sales Records")
    if st.button("Export to CSV"):
        df.to_csv("sales_records.csv", index=False)
        st.success("Sales records exported to CSV!")
