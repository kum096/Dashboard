import streamlit as st
import pandas as pd
from datetime import datetime

from backend import get_all_shipments, submit_shipment, delete_shipment
from utils import parse_date, format_date, parse_time, format_time

# Streamlit config
st.set_page_config(page_title="Admin Dashboard - TrackNest", layout="centered")

def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("🔐 TrackNest Admin Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.button("Login")

        if login_button:
            if username == "trackit" and password == "track123":
                st.session_state.logged_in = True
                st.success("Login successful! Please wait...")
            else:
                st.error("Invalid username or password")

    else:
        st.title("📦 TrackNest Logistics - Admin Dashboard")
        st.caption("Manage shipments in real-time")

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.experimental_rerun()

        # Tabs
        view_tab, add_tab = st.tabs(["📋 View / Edit Shipments", "➕ Add Shipment"])

        # --- View Shipments --- #
        with view_tab:
            shipments = get_all_shipments()
            
            if shipments:
                df = pd.DataFrame(shipments)

                try:
                    df_display = df[["tracking_number", "status", "port_of_loading", "port_of_discharge", "expected_arrival_date"]]
                    df_display.columns = ["Tracking #", "Status", "Origin", "Destination", "Expected Delivery"]
                    st.dataframe(df_display, use_container_width=True)
                except KeyError as e:
                    st.error(f"Missing columns in API data: {e}")
                    st.stop()

                selected = st.selectbox("Select a tracking number to edit/delete", df["tracking_number"])
                selected_data = df[df["tracking_number"] == selected].iloc[0]

                with st.expander("Edit Shipment Details"):
                    with st.form("update_form"):
                        st.subheader("Sender Information")
                        sender_name = st.text_input("Sender Name", selected_data.get("sender_name", ""))
                        sender_email = st.text_input("Sender Email", selected_data.get("sender_email", ""))
                        sender_number = st.text_input("Sender Phone Number", selected_data.get("sender_number", ""))
                        sender_address = st.text_area("Sender Address", selected_data.get("sender_address", ""))

                        st.subheader("Receiver Information")
                        receiver_name = st.text_input("Receiver Name", selected_data.get("receiver_name", ""))
                        receiver_email = st.text_input("Receiver Email", selected_data.get("receiver_email", ""))
                        receiver_number = st.text_input("Receiver Phone Number", selected_data.get("receiver_number", ""))
                        receiver_address = st.text_area("Receiver Address", selected_data.get("receiver_address", ""))

                        st.subheader("Shipment Information")
                        product_description = st.text_area("Product Description", selected_data.get("product_description", ""))
                        quantity = st.text_input("Quantity", selected_data.get("quantity", ""))
                        weight = st.text_input("Weight", selected_data.get("weight", ""))
                        port_of_loading = st.text_input("Port of Loading", selected_data.get("port_of_loading", ""))
                        port_of_discharge = st.text_input("Port of Discharge", selected_data.get("port_of_discharge", ""))
                        shipping_mode = st.text_input("Shipping Mode", selected_data.get("shipping_mode", ""))
                        voyage = st.text_input("Voyage Number", selected_data.get("voyage", ""))
                        carrier = st.text_input("Carrier", selected_data.get("carrier", ""))
                        vessel = st.text_input("Vessel Name", selected_data.get("vessel", ""))
                        status = st.selectbox("Status", ["pending", "in_transit", "delivered", "canceled"], index=["pending", "in_transit", "delivered", "canceled"].index(selected_data.get("status", "pending")))

                        departure_date = st.date_input("Departure Date", parse_date(selected_data.get("departure_date")) or datetime.today().date())
                        expected_arrival_date = st.date_input("Expected Arrival Date", parse_date(selected_data.get("expected_arrival_date")) or datetime.today().date())
                        registration_date = st.date_input("Registration Date", parse_date(selected_data.get("registration_date")) or datetime.today().date())

                        st.subheader("Current Status")
                        current_location = st.text_input("Current Location", selected_data.get("current_location", ""))
                        latest_status_date = st.date_input("Latest Status Date", parse_date(selected_data.get("latest_status_date")) or datetime.today().date())
                        default_time = parse_time(selected_data.get("latest_status_time")) or datetime.strptime("12:00", "%H:%M").time()
                        latest_status_time = st.time_input("Latest Status Time", default_time)
                        next_transit_port = st.text_input("Next Transit Port", selected_data.get("next_transit_port", ""))

                        st.subheader("Coordinates")
                        current_lat = st.text_input("Current Latitude", selected_data.get("current_location_coords", {}).get("latitude", ""))
                        current_lon = st.text_input("Current Longitude", selected_data.get("current_location_coords", {}).get("longitude", ""))
                        dest_lat = st.text_input("Destination Latitude", selected_data.get("destination_coords", {}).get("latitude", ""))
                        dest_lon = st.text_input("Destination Longitude", selected_data.get("destination_coords", {}).get("longitude", ""))

                        submitted = st.form_submit_button("Update Shipment")

                        if submitted:
                           try:
        # Parse coordinates safely to floats or None if empty
                                 def parse_coord(value):
                                     if value is None or value == "" or str(value).strip() == "":
                                         return None
                                     return float(value)
                                 
                                 data = {
                                    "tracking_number": selected,
                                    "sender_name": sender_name,
                                    "sender_email": sender_email,
                                    "sender_number": sender_number,
                                    "sender_address": sender_address,
                                    "receiver_name": receiver_name,
                                    "receiver_email": receiver_email,
                                    "receiver_number": receiver_number,
                                    "receiver_address": receiver_address,
                                    "product_description": product_description,
                                    "quantity": quantity,
                                    "weight": weight,
                                    "port_of_loading": port_of_loading,
                                    "port_of_discharge": port_of_discharge,
                                    "shipping_mode": shipping_mode,
                                    "voyage": voyage,
                                    "carrier": carrier,
                                    "vessel": vessel,
                                    "status": status,
                                    "departure_date": format_date(departure_date),
                                    "expected_arrival_date": format_date(expected_arrival_date),
                                    "registration_date": format_date(registration_date),
                                    "current_location": current_location,
                                    "latest_status_date": format_date(latest_status_date),
                                    "latest_status_time": format_time(latest_status_time),
                                    "next_transit_port": next_transit_port,
                                    "current_location_coords": {
                                       "latitude": parse_coord(current_lat),
                                       "longitude": parse_coord(current_lon)
                                    },
                                    "destination_coords": {
                                        "latitude": parse_coord(dest_lat),
                                        "longitude": parse_coord(dest_lon)
                                    }
                                }
                                 submit_shipment(data, update=True)
                           except ValueError:
                                   st.error("Latitude and Longitude values must be valid numbers.")  

                if st.button("Delete This Shipment", type="primary"):
                    delete_shipment(selected)

        # --- Add Shipment --- #
        with add_tab:
            with st.form("add_form"):
                st.subheader("Sender Information")
                sender_name = st.text_input("Sender Name")
                sender_email = st.text_input("Sender Email")
                sender_number = st.text_input("Sender Phone Number")
                sender_address = st.text_area("Sender Address")

                st.subheader("Receiver Information")
                receiver_name = st.text_input("Receiver Name")
                receiver_email = st.text_input("Receiver Email")
                receiver_number = st.text_input("Receiver Phone Number")
                receiver_address = st.text_area("Receiver Address")

                st.subheader("Shipment Information")
                tracking_number = st.text_input("Tracking Number (e.g. TN1234567890)")
                product_description = st.text_area("Product Description")
                quantity = st.text_input("Quantity", "1 pallet")
                weight = st.text_input("Weight", "400 kg")
                port_of_loading = st.text_input("Port of Loading")
                port_of_discharge = st.text_input("Port of Discharge")
                shipping_mode = st.text_input("Shipping Mode")
                voyage = st.text_input("Voyage Number")
                carrier = st.text_input("Carrier")
                vessel = st.text_input("Vessel Name")
                status = st.selectbox("Status", ["pending", "in_transit", "delivered", "canceled"])

                departure_date = st.date_input("Departure Date")
                expected_arrival_date = st.date_input("Expected Arrival Date")
                registration_date = st.date_input("Registration Date")

                st.subheader("Current Status")
                current_location = st.text_input("Current Location")
                latest_status_date = st.date_input("Latest Status Date")
                latest_status_time = st.time_input("Latest Status Time")
                next_transit_port = st.text_input("Next Transit Port")

                st.subheader("Coordinates")
                current_lat = st.text_input("Current Latitude")
                current_lon = st.text_input("Current Longitude")
                dest_lat = st.text_input("Destination Latitude")
                dest_lon = st.text_input("Destination Longitude")

                submit = st.form_submit_button("Add Shipment")

                if submit:
                    if not tracking_number:
                        st.error("Tracking number is required.")
                    else:
                        data = {
                            "tracking_number": tracking_number,
                            "sender_name": sender_name,
                            "sender_email": sender_email,
                            "sender_number": sender_number,
                            "sender_address": sender_address,
                            "receiver_name": receiver_name,
                            "receiver_email": receiver_email,
                            "receiver_number": receiver_number,
                            "receiver_address": receiver_address,
                            "product_description": product_description,
                            "quantity": quantity,
                            "weight": weight,
                            "port_of_loading": port_of_loading,
                            "port_of_discharge": port_of_discharge,
                            "shipping_mode": shipping_mode,
                            "voyage": voyage,
                            "carrier": carrier,
                            "vessel": vessel,
                            "status": status,
                            "departure_date": format_date(departure_date),
                            "expected_arrival_date": format_date(expected_arrival_date),
                            "registration_date": format_date(registration_date),
                            "current_location": current_location,
                            "latest_status_date": format_date(latest_status_date),
                            "latest_status_time": str(latest_status_time),
                            "next_transit_port": next_transit_port,
                            "current_location_coords": {
                                "latitude": current_lat,
                                "longitude": current_lon
                            },
                            "destination_coords": {
                                "latitude": dest_lat,
                                "longitude": dest_lon
                            }
                        }
                        submit_shipment(data)

if __name__ == "__main__":
    main()