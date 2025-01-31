# utils.py
import pandas as pd

def filter_sales_records(df, date_range=None, distributor=None, payment_status=None):
    """
    Filter sales records based on date range, distributor, and payment status.
    """
    if date_range:
        df = df[(df["Date"] >= date_range[0]) & (df["Date"] <= date_range[1])]
    if distributor:
        df = df[df["Assigned Distributor"] == distributor]
    if payment_status:
        df = df[df["Payment Status"] == payment_status]
    return df

def export_to_csv(df, filename="sales_records.csv"):
    """
    Export a DataFrame to a CSV file.
    """
    df.to_csv(filename, index=False)
