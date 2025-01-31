# app.py
import streamlit as st
from database import SessionLocal
from auth import authenticate_user
from models import User, SalesRecord, UserRole
import pandas as pd
import plotly.express as px

# Session state for user authentication
if "user" not in st.session_state:
    st.session_state.user = None

# Login form
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        db = SessionLocal()
        user = authenticate_user(db, username, password)
        if user:
            st.session_state.user = user
            st.success(f"Logged in as {user.username} ({user.role.value})")
        else:
            st.error("Invalid username or password")

# Admin dashboard
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
        assigned_distributor_id = st.selectbox("Assign to Distributor", [user.id for user in db.query(User).filter(User.role == UserRole.DISTRIBUTOR).all()])
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

# Distributor dashboard
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

# Main app logic
def main():
    if st.session_state.user is None:
        login()
    else:
        if st.session_state.user.role == UserRole.ADMIN:
            admin_dashboard()
        elif st.session_state.user.role == UserRole.DISTRIBUTOR:
            distributor_dashboard()

if __name__ == "__main__":
    main()
