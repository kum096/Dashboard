import requests
import streamlit as st

# Your deployed API base URL
API_URL = "https://backend-umdv.onrender.com/api/v1/shipments"

# Get all shipments
def get_all_shipments():
    try:
        res = requests.get(API_URL)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"Error fetching shipments: {e}")
        return []

# Add or update shipment
def submit_shipment(data, update=False):
    try:
        if update:
            # Call the new full update route
            res = requests.put(f"{API_URL}/fullupdate/{data['tracking_number']}", json=data)
        else:
            res = requests.post(API_URL, json=data)
        res.raise_for_status()
        st.success("Shipment successfully submitted!")
    except Exception as e:
        st.error(f"Error submitting shipment: {e}")

# Delete a shipment
def delete_shipment(tracking_number):
    try:
        res = requests.delete(f"{API_URL}/tracking/{tracking_number}")
        res.raise_for_status()
        st.success("Shipment deleted.")
    except Exception as e:
        st.error(f"Delete failed: {e}")
