import streamlit as st
import pandas as pd
from datetime import datetime

from backend import get_all_shipments, submit_shipment, delete_shipment
from utils import parse_date, format_date

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
                # Instead of rerun, use st.experimental_set_query_params or
                # just return and let Streamlit rerun naturally
                st.success("Login successful! Please wait...")
            else:
                st.error("Invalid username or password")

    else:
        st.title("📦 TrackNest Logistics - Admin Dashboard")
        st.caption("Manage shipments in real-time")

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.experimental_rerun()  # <-- We will fix this in a second

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
                        status = st.selectbox(
                            "Status",
                            ["pending", "in_transit", "delivered", "canceled"],
                            index=["pending", "in_transit", "delivered", "canceled"].index(selected_data.get("status", "pending"))
                        )

                        origin = st.text_input("Origin", selected_data.get("port_of_loading", ""))
                        destination = st.text_input("Destination", selected_data.get("port_of_discharge", ""))

                        expected_str = selected_data.get("expected_arrival_date")
                        expected_delivery = parse_date(expected_str) or datetime.today().date()
                        expected_delivery = st.date_input("Expected Delivery", expected_delivery)

                        current_location = st.text_input("Current Location", selected_data.get("current_location", ""))

                        submitted = st.form_submit_button("Update Shipment")
                        if submitted:
                            data = {
                                "tracking_number": selected,
                                "status": status,
                                "port_of_loading": origin,
                                "port_of_discharge": destination,
                                "expected_arrival_date": format_date(expected_delivery),
                                "current_location": current_location
                            }
                            submit_shipment(data, update=True)

                if st.button("Delete This Shipment", type="primary"):
                    delete_shipment(selected)

            else:
                st.warning("No shipments found.")

        # --- Add Shipment --- #
        with add_tab:
            with st.form("add_form"):
                tracking_number = st.text_input("Tracking Number (e.g. TN1234567890)")
                status = st.selectbox("Status", ["pending", "in_transit", "delivered", "canceled"])
                origin = st.text_input("Origin")
                destination = st.text_input("Destination")
                expected_delivery = st.date_input("Expected Delivery")
                current_location = st.text_input("Current Location")

                submit = st.form_submit_button("Add Shipment")
                if submit:
                    if not tracking_number:
                        st.error("Tracking number is required.")
                    else:
                        data = {
                            "tracking_number": tracking_number,
                            "status": status,
                            "port_of_loading": origin,
                            "port_of_discharge": destination,
                            "expected_arrival_date": format_date(expected_delivery),
                            "current_location": current_location
                        }
                        submit_shipment(data)


if __name__ == "__main__":
    main()
