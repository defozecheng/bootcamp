import streamlit as st
from agents.chat_agent import create_chat_agent
from agents.customer_chat_agent import create_customer_chat_agent
import requests
import pandas as pd
from datetime import datetime
import json
import os

CAR_MODELS = {
    "BMW": ["1 Series", "2 Series", "3 Series", "5 Series", "7 Series", "X1", "X3", "X5", "X6", "iX"],
    "BYD": ["Atto 2", "Atto 3", "Dolphin", "Seal", "Seal 6", "Sealion 5", "Sealion 7", "M6"],
    "Chery": ["Tiggo 7 Pro", "Tiggo 8 Pro", "Tiggo Cross", "O5", "E5"],
    "GWM/Haval": ["Haval H6", "Haval H6 HEV", "Haval H6 PHEV", "Haval Jolion", "Ora Good Cat", "Ora 07", "Tank 300", "Tank 500"],
    "Honda": ["City", "City Hatchback", "Civic", "Accord", "HR-V", "CR-V", "BR-V", "WR-V"],
    "iCAUR": ["03", "V23"],
    "Isuzu": ["D-Max", "MU-X"],
    "Jetour": ["Dashing", "VT9", "T2"],
    "Leapmotor": ["C10", "B10"],
    "Lexus": ["ES", "IS", "NX", "RX", "UX", "LM", "RZ", "LBX"],
    "Mazda": ["Mazda2", "Mazda3", "Mazda6", "CX-3", "CX-30", "CX-5", "CX-8", "CX-60", "CX-80"],
    "Mercedes-Benz": ["A-Class", "C-Class", "E-Class", "S-Class", "CLA", "GLA", "GLC", "GLE", "EQA", "EQE"],
    "Mitsubishi": ["Triton", "Xpander", "Outlander", "ASX", "Attrage"],
    "Nissan": ["Almera", "Serena", "X-Trail", "Navara", "Kicks", "Leaf"],
    "Omoda/Jaecoo": ["Omoda 5", "Omoda E5", "Jaecoo J7", "Jaecoo J7 PHEV", "Jaecoo J8"],
    "Perodua": ["Axia", "Bezza", "Myvi", "Alza", "Ativa", "Aruz", "Kancil", "Kelisa", "Viva"],
    "Proton": ["Saga", "Persona", "Iriz", "S70", "X50", "X70", "X90", "e.MAS 5", "e.MAS 7"],
    "Tesla": ["Model 3", "Model Y", "Model S", "Model X"],
    "Toyota": ["Vios", "Yaris", "Corolla", "Corolla Cross", "Camry", "Hilux", "Fortuner", "Innova Zenix", "Veloz", "Alphard"],
    "Zeekr": ["X", "7X", "009"]
}

st.set_page_config(
    page_title="Car Management Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded")

API_BASE_URL = "http://127.0.0.1:8000"

def check_api_connection():
    try:
        response = requests.get(f"{API_BASE_URL}/")
        return response.status_code == 200
    except:
        return False

def create_car(name, phone, car_plate, brand, model, year, current_mileage):
    try:
        response = requests.post(
            f"{API_BASE_URL}/cars/",
            json={
                "name": name, 
                "phone": phone, 
                "car_plate": car_plate, 
                "brand": brand, "model": model, 
                "year":year, 
                "current_mileage": current_mileage}
        )
        return response.json(), response.status_code == 201
    except Exception as e:
        return {"error": str(e)}, False

def get_all_cars():
    try:
        response = requests.get(f"{API_BASE_URL}/cars/")
        if response.status_code == 200:
            return response.json(), True
        return [], False
    except Exception as e:
        return [], False

def get_car(car_id):
    try:
        response = requests.get(f"{API_BASE_URL}/cars/{car_id}")
        return response.json(), response.status_code == 200
    except Exception as e:
        return {"error": str(e)}, False

def update_car(car_id, name, phone, car_plate, brand, model, year, current_mileage):
    try:
        response = requests.put(
            f"{API_BASE_URL}/cars/{car_id}",
            json={
                "name": name, 
                "phone": phone, 
                "car_plate": car_plate, 
                "brand": brand, 
                "model": model, 
                "year":year, 
                "current_mileage": current_mileage}
        )
        return response.json(), response.status_code == 200
    except Exception as e:
        return {"error": str(e)}, False

def delete_car(car_id):
    try:
        response = requests.delete(f"{API_BASE_URL}/cars/{car_id}")
        return response.json(), response.status_code == 200
    except Exception as e:
        return {"error": str(e)}, False

def create_maintenance_record(car_id, sv_type, sv_date, next_service_date, sv_mileage, sv_interval, cost, paid_amount,notes):
    try:
        response = requests.post(
            f"{API_BASE_URL}/maintenance_records/",
            json={
                "car_id": car_id, 
                "sv_type": sv_type,
                "sv_date": sv_date.isoformat(),
                "next_service_date": next_service_date.isoformat(), 
                "sv_mileage": sv_mileage,
                "sv_interval": sv_interval,
                "cost": cost,
                "paid_amount": paid_amount,
                "notes": notes}
        )
        return response.json(), response.status_code == 201
    except Exception as e:
        return {"error": str(e)}, False

def get_car_maintenance_records(car_id):
    try:
        response = requests.get(f"{API_BASE_URL}/cars/{car_id}/maintenance_records")
        if response.status_code == 200:
            return response.json(), True
        return [], False
    except Exception as e:
        return [], False

def get_maintenance_record(record_id):
    try:
        response = requests.get(f"{API_BASE_URL}/maintenance_records/{record_id}")
        return response.json(), response.status_code == 200
    except Exception as e:
        return {"error": str(e)}, False

def update_maintenance_record(record_id, car_id, sv_type, sv_date, next_service_date, sv_mileage, sv_interval, cost, paid_amount, notes):
    try:
        response = requests.put(
            f"{API_BASE_URL}/maintenance_records/{record_id}",
            json={
                "car_id": car_id,
                "sv_type": sv_type,
                "sv_date": sv_date.isoformat(), 
                "next_service_date": next_service_date.isoformat(),
                "sv_mileage": sv_mileage,
                "sv_interval": sv_interval,
                "cost": cost,
                "paid_amount": paid_amount,
                "notes": notes}
        )
        return response.json(), response.status_code == 200
    except Exception as e:
        return {"error": str(e)}, False

def delete_maintenance_record(record_id):
    try:
        response = requests.delete(f"{API_BASE_URL}/maintenance_records/{record_id}")
        return response.json(), response.status_code == 200
    except Exception as e:
        return {"error": str(e)}, False

def main():
    st.title("Car Service Management")
    st.markdown("---")

    if not check_api_connection():
        st.error("❌ Cannot connect to FASTAPI server. Please make sure it's running on http://127.0.0.1:8000")
        st.info("Run: 'uvicorn main:app --reload' to start the server")
        return

    st.success("✅ Connected to FASTAPI server")

    st.sidebar.title("Navigation")

    if "staff_logged_in" not in st.session_state:
        st.session_state.staff_logged_in = False

    if "customer_car" not in st.session_state:
        st.session_state.customer_car = None

    if st.session_state.staff_logged_in:
        page = st.sidebar.radio(
            "Select Page",
            [
                "🚗 Car",
                "🛠️ Maintenance Records",
                "📊 Dashboard",
                "🤖 Car Assistant"
            ]
        )

        if st.sidebar.button("Staff Logout"):
            st.session_state.staff_logged_in = False
            st.rerun()


    elif st.session_state.customer_car is not None:
        page = st.sidebar.radio(
            "Select Page",
            [
                "🚗 My Car",
                "🔔 Service Status",
                "📋 Maintenance History",
                "🤖 Customer Car Assistant"
            ]
        )

        if st.sidebar.button("Customer Logout"):
            st.session_state.customer_car = None
            st.session_state.customer_messages = []
            st.rerun()

    else:
        login_type = st.sidebar.radio("Select Login", ["👤 Customer Login", "🔐 Staff Login"])

        if login_type == "👤 Customer Login":
            page = "👤 Customer Portal"
        elif login_type == "🔐 Staff Login":
            page = "🔐 Staff Login"

            st.header("🔐 Staff Login")
            st.write("Login to access the staff management system.")

            staff_id = st.text_input("Staff ID", autocomplete="off")
            staff_password = st.text_input("Staff Password", type="password", autocomplete="new-password")
            if st.button("Staff Login", type="primary"):
                if (
                    staff_id == os.getenv("STAFF_ID")
                    and staff_password == os.getenv("STAFF_PASSWORD")
                ):
                    st.session_state.staff_logged_in = True
                    st.success("✅ Staff login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid Staff ID or password")
        
    if page == "🚗 Car":
        cars_page()
    elif page == "🛠️ Maintenance Records":
        maintenance_record_page()
    elif page == "📊 Dashboard":
        dashboard_page()
    elif page == "🤖 Car Assistant":
        car_assistant_page()
    elif page == "👤 Customer Portal":
        customer_portal_page()
    elif page == "🔐 Staff Login":pass
    elif page == "🚗 My Car": 
        customer_car_page()
    elif page == "🔔 Service Status":
        customer_service_status_page()
    elif page == "📋 Maintenance History":
        customer_maintenance_history_page()
    elif page == "🤖 Customer Car Assistant":
        customer_assistant_page()


def cars_page():
    st.header("🚗 Car Management")

    tab1, tab2, tab3 = st.tabs(["Add Car","View Cars", "Manage Car"])

    with tab1:
        st.subheader("➕ Add New Car")
        
        col1, col2,col3 = st.columns(3)
        with col1:
            name = st.text_input("Name", placeholder="Enter car owner name")
            phone = st.text_input("Phone Number", placeholder="Enter phone number")
            car_plate = st.text_input("Car Plate Number", placeholder="Enter car plate number")
        with col2:
            brand = st.selectbox("Select Car Brand", list(CAR_MODELS.keys()), key="create_brand")
            model = st.selectbox("Select Car Model", CAR_MODELS[brand], key="create_model")
        with col3:
            year = st.number_input("Year", min_value=1950,max_value=2026, value=2025)
            current_mileage = st.number_input("Current Mileage",placeholder=" Enter current mileage", min_value=0, step=1000)

        if st.button("Create Car", type="primary"):
            if name and phone and car_plate and brand and model:
                result, success = create_car(name, phone, car_plate, brand, model, year, current_mileage)

                if success:
                    st.success(f"✅ Car created successfully! ID: {result.get('car_id')}")
                else:
                    st.error(f"❌ Error: {result.get('detail', 'Unknown error')}")
            else:
                st.error("❌ Please fill in all fields")

    with tab2:
        st.subheader("🗂️ View Car Details")
        cars, cars_success = get_all_cars()
        if cars_success and cars:
            df = pd.DataFrame(cars)
            df['created_at'] = pd.to_datetime(df["created_at"]).dt.strftime('%Y-%m-%d %H:%M:%S')
            st.dataframe(
                df[['id', 'name', 'phone', 'car_plate', 'brand', 'model', 'year', 'current_mileage', 'created_at']],
                use_container_width=True,
                hide_index=True
            )
            st.info(f"Total cars: {len(cars)}")

            st.divider()
            st.subheader("🔍 View Individual Car")
            car_options = {
                f"{car['car_plate']} - {car['brand']} {car['model']}": car["id"]for car in cars}
            selected_car = st.selectbox("Select Car", options=list(car_options.keys()),key="view_car")
            if st.button("View Car Details"):
                selected_car_id = car_options[selected_car]
                car, car_success = get_car(selected_car_id)
                if car_success:
                        st.write("**Name:**", car.get("name"))
                        st.write("**Phone:**", car.get("phone"))
                        st.write("**Car Plate:**", car.get("car_plate"))
                        st.write("**Brand:**", car.get("brand"))
                        st.write("**Model:**", car.get("model"))
                        st.write("**Year:**", car.get("year"))
                        st.write("**Current Mileage:**", car.get("current_mileage"))
                else:
                    st.error(f"❌ Error: {car.get('detail', 'Car not found')}")
        else:
            st.info("No cars found")

    with tab3:
        st.subheader("⚙️ Manage Cars")
        cars, cars_success = get_all_cars()

        if cars_success and cars:
            car_options = {f"{car['car_plate']} - {car['brand']} {car['model']}": car["id"]for car in cars}
            selected_car_display = st.selectbox("Select Car", options=list(car_options.keys()),key="manage_car")

            if selected_car_display:
                selected_car_id = car_options[selected_car_display]
                selected_car = next(( car for car in cars if car['id'] == selected_car_id),None)

                if selected_car:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Update Car Data**")
                        brand_list = list(CAR_MODELS.keys())
                        new_brand = st.selectbox("Select Car Brand", brand_list, index=brand_list.index(selected_car["brand"]), key=f"update_brand_{selected_car_id}")
                        model_list = CAR_MODELS[new_brand]
                        if selected_car["model"] in model_list:
                            model_index = model_list.index(selected_car["model"])
                        else:
                            model_index = 0
                        new_model = st.selectbox("Select Car Model", model_list, index=model_index, key=f"update_model_{selected_car_id}")
                        with st.form(f"update_car_form_{selected_car_id}"):
                            new_name = st.text_input("Name", value=selected_car['name'])
                            new_phone = st.text_input("Phone Number", value=selected_car['phone'])
                            new_car_plate = st.text_input("Car Plate Number", value=selected_car['car_plate'])
                            new_year = st.number_input("Year", min_value=1950,max_value=2026, value=selected_car['year'])
                            new_current_mileage = st.number_input("Current Mileage", value=selected_car['current_mileage'], min_value=0, step=1000)
                            if st.form_submit_button("Update Car", type="primary"):
                                result, update_success = update_car(selected_car_id, new_name, new_phone, new_car_plate, new_brand, new_model, new_year, new_current_mileage)
                                if update_success:
                                    st.success("✅ Car updated successfully!")
                                else:
                                    st.error(f"❌ Error: {result.get('detail','Unknown error')}")
                    with col2:
                        st.write("**Delete Car**")
                        st.warning("⚠️ This will delete all the car data and maintenance records!")
                        if st.button("Delete Car", type="secondary"):
                            result, delete_success = delete_car(selected_car_id)
                            if delete_success:
                                st.success("✅ Car deleted successfully!")
                                st.rerun()
                            else:
                                st.error(f"❌ Error: {result.get('detail', 'Unknown error')}")

def maintenance_record_page():
    st.header("🛠️ Maintenance Records")

    cars, cars_success = get_all_cars()

    if not cars_success or not cars:
        st.warning("⚠️ No cars found. Please create a car first")
        return

    car_options = {
        f"{car['car_plate']} - {car['brand']} {car['model']}": car["id"]
        for car in cars
    }

    tab1, tab2, tab3 = st.tabs(["Create Maintenance Record", "View Maintenance Record", "Manage Maintenance Record"])

    with tab1:
        st.subheader("➕ Create New Maintenance Record")
        selected_car_display = st.selectbox("Select Car", options=list(car_options.keys()),key="create_record_car")
        selected_car_id = car_options[selected_car_display]
        selected_car = next((car for car in cars if car["id"] == selected_car_id),None)
        if selected_car:st.info(f"🚗 Current Mileage: {selected_car['current_mileage']:,} km")


        types = ["Engine Oil", "Oil Filter", "Air Filter Cleaning", "Tyre Pressure Check",
                "Engine Air Filter Replacement", "Cabin Air Filter Replacement", "Tyre Rotation and Balancing",
                "Wheel Alignment", "Brake Pad Inspection","AT Fluid Change", "Brake Fluid FLush",
                " Engine Coolant Flush", "Spark Plug Replacement", "Fuel Filter Replacement"]
        sv_type = st.multiselect("Select Service Type", types)
        sv_date = st.date_input("Service Date")
        next_service_date = st.date_input("Next Service Date")
        sv_mileage = st.number_input("Current Mileage at Service (km)", min_value=0, step=1000, value=int(selected_car["current_mileage"]), key=f"service_mileage_{selected_car_id}")
        sv_interval= st.selectbox("Service Interval (km)", [5000,10000,15000,20000])
        next_service_mileage = sv_mileage + sv_interval
        st.info(f"Next Service Mileage: {next_service_mileage:,} km")
        cost = st.number_input("Cost (RM)", min_value=0.0, value=0.0, step=10.0)
        paid_amount = st.number_input("Paid Amount (RM)", min_value=0.0, value=0.0, step=10.0)
        notes = st.text_input("Notes", placeholder="Remarks")
        submitted = st.button("Create Maintenance Record", type="primary")

        if submitted:
            if paid_amount > cost:
                st.error("❌ Paid Amount cannot be greater than Cost.")
            elif next_service_date < sv_date:
                st.error("❌ Next Service Date cannot be earlier than Service Date.")
            elif selected_car_display and sv_type and sv_date and next_service_date:
                car_id = selected_car_id
                sv_date_datetime = datetime.combine(sv_date, datetime.min.time())
                next_service_date_datetime = datetime.combine(next_service_date, datetime.min.time())
                result, record_success = create_maintenance_record(car_id, sv_type, sv_date_datetime, next_service_date_datetime, sv_mileage, sv_interval, cost, paid_amount, notes)
                if record_success:
                    st.success(f"✅ Maintenance record created successfully! ID: {result.get('record_id')}")
                else:
                    st.error(f"❌ Error: {result.get('detail', 'Unknown error')}")
            else:
                st.error("❌ Please fill in all fields")


    with tab2:
        st.subheader("All Maintenance Records")

        selected_view_car = st.selectbox("Select Car", options=list(car_options.keys()), key="view_record_car")

        if selected_view_car:
            car_id = car_options[selected_view_car]
            maintenance_records, records_success = get_car_maintenance_records(car_id)

            if records_success and maintenance_records:
                for maintenance_record in maintenance_records:
                    service_types = ", ".join(maintenance_record["sv_type"])
                    with st.expander(f" {service_types}"f"(ID:{maintenance_record['record_id'][:8]}...)"):
                            service_date = pd.to_datetime(maintenance_record["sv_date"]).strftime("%Y-%m-%d")
                            st.write(f"**Service Date:** {service_date}")
                            st.write(f"**Current Mileage at Service:** {maintenance_record['sv_mileage']:,}km")
                            st.write(f"**Service Interval** {maintenance_record['sv_interval']:,}km")
                            next_service_mileage = (maintenance_record["sv_mileage"] + maintenance_record["sv_interval"])
                            st.write(f"**Next Service Mileage:** {next_service_mileage:,} km")
                            st.write(f"**Cost:** RM {maintenance_record['cost']:,.2f}")
                            st.write( f"**Paid Amount:** RM {maintenance_record.get('paid_amount', 0.0):,.2f}")
                            balance = (maintenance_record["cost"] - maintenance_record.get("paid_amount", 0.0))
                            st.write(f"**Balance:** RM {balance:,.2f}")
                            st.write(f"**Notes:** {maintenance_record['notes']}")
                            created_at = pd.to_datetime(maintenance_record["created_at"]).strftime("%Y-%m-%d %H:%M:%S")
                            st.write("**Created:**", created_at)
                st.info(f"Total maintenance records: {len(maintenance_records)}")
            else:
                st.info("No maintenance records found")

    with tab3:
        st.subheader("Manage Maintenance Records")

        selected_manage_car = st.selectbox("Select Car", options=list(car_options.keys()), key="manage_record_car")
        if selected_manage_car:
            car_id = car_options[selected_manage_car]
            maintenance_records, records_success = get_car_maintenance_records(car_id)

            if records_success and maintenance_records:
                record_options = {f"{', '.join(record['sv_type'])} - {record['sv_date']}": record["record_id"]
                                    for record in maintenance_records
                                    }
                selected_record_display = st.selectbox("Select Maintenance Record", options=list(record_options.keys()),key="manage_maintenance_record")
                if selected_record_display:
                    selected_record_id = record_options[selected_record_display]
                    selected_record = next(( record for record in maintenance_records if record["record_id"] == selected_record_id),None)

                if selected_record:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Update Maintenance Record**")
                        types = ["Engine Oil", "Oil Filter", "Air Filter Cleaning", "Tyre Pressure Check",
                                "Engine Air Filter Replacement", "Cabin Air Filter Replacement", "Tyre Rotation and Balancing",
                                "Wheel Alignment", "Brake Pad Inspection","AT Fluid Change", "Brake Fluid FLush",
                                " Engine Coolant Flush", "Spark Plug Replacement", "Fuel Filter Replacement"]
                        intervals = [5000, 10000, 15000, 20000]
                        with st.form(f"update_record_form_{selected_record_id}"):
                            existing_next_service_date = selected_record.get("next_service_date")
                            if existing_next_service_date:
                                next_service_date_value = pd.to_datetime(
                                    existing_next_service_date
                            ).date()
                            else:
                                next_service_date_value = pd.to_datetime(
                                    selected_record["sv_date"]
                                ).date()
                            new_sv_type = st.multiselect("Service type", types, default=(selected_record['sv_type']))
                            new_sv_date = st.date_input("Service date", value=pd.to_datetime(selected_record['sv_date']).date())
                            new_next_service_date = st.date_input("Next Service Date", value=next_service_date_value)
                            new_sv_mileage = st.number_input("Current Mileage at Service (km)", value=selected_record['sv_mileage'], min_value=0,step=1000)
                            new_sv_interval = st.selectbox("Service Interval (km)", intervals, index=intervals.index(selected_record['sv_interval']))
                            new_next_service_mileage = (new_sv_mileage + new_sv_interval)
                            st.info(f"Next Service Mileage: {new_next_service_mileage:,} km")
                            new_cost = st.number_input("Cost (RM)", min_value=0.0, value=float(selected_record['cost']), step=10.0)
                            new_paid_amount = st.number_input("Paid Amount (RM)", min_value=0.0, value=float(selected_record.get("paid_amount", 0.0)), step=10.0)
                            new_notes = st.text_input("Notes", value=selected_record['notes'])
                            if st.form_submit_button("Update Record", type="primary"):
                                if new_paid_amount > new_cost:
                                    st.error("❌ Paid Amount cannot be greater than Cost.")
                                elif new_next_service_date < new_sv_date:
                                    st.error("❌ Next Service Date cannot be earlier than Service Date.")
                                else: 
                                    new_sv_date_datetime = datetime.combine(new_sv_date,datetime.min.time())
                                    new_next_service_date_datetime = datetime.combine(new_next_service_date, datetime.min.time())
                                    result, update_success = update_maintenance_record(selected_record_id, car_id, new_sv_type, new_sv_date_datetime, new_next_service_date_datetime, new_sv_mileage, new_sv_interval, new_cost, new_paid_amount, new_notes)
                                    if update_success:
                                        st.success("✅ Record updated successfully!")
                                    else:
                                        st.error(f"❌ Error: {result.get('detail','Unknown error')}")
                    with col2:
                        st.write("**Delete Record**")
                        st.warning("⚠️ This will delete this maintenance records!")
                        if st.button("Delete Record", type="secondary"):
                            result, delete_success = delete_maintenance_record(selected_record_id)
                            if delete_success:
                                st.success("✅ Record deleted successfully!")
                                st.rerun()
                            else:
                                st.error(f"❌ Error: {result.get('detail', 'Unknown error')}")

def dashboard_page():
    st.header("📊 Dashboard")

    cars, cars_success = get_all_cars()
    if not cars_success:
        st.error("❌ Failed to load car data")
        return

    all_records = []

    for car in cars:
        records, records_success = get_car_maintenance_records(car["id"])

        if records_success:
            for record in records:
                record_data = record.copy()

                record_data["car_plate"] = car["car_plate"]
                record_data["brand"] = car["brand"]
                record_data["model"] = car["model"]
                record_data["current_mileage"] = car["current_mileage"]

                all_records.append(record_data)

    total_cars = len(cars)
    total_records = len(all_records)
    total_cost = sum(float(record.get("cost", 0))
        for record in all_records
    )

    average_cost = (total_cost / total_records
        if total_records > 0
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🚗 Total Cars", total_cars)

    with col2:
        st.metric("🔧 Maintenance Records", total_records)

    with col3:
        st.metric( "💰 Estimated Service Value", f"RM {total_cost:,.2f}")

    with col4:
        st.metric("📊 Average Service Cost", f"RM {average_cost:,.2f}")

    total_paid = sum(float(record.get("paid_amount", 0))
        for record in all_records
    )
    outstanding = total_cost - total_paid

    st.subheader("💰 Revenue Summary")

    rev1, rev2, rev3 = st.columns(3)
    with rev1:
        st.metric("Estimated Revenue", f"RM {total_cost:,.2f}")

    with rev2:
        st.metric("Paid Revenue", f"RM {total_paid:,.2f}")

    with rev3:
        st.metric("Outstanding", f"RM {outstanding:,.2f}")

    st.markdown("---")

    st.subheader("🔔 Next Service Overview")

    service_status = []
    for car in cars:
        car_records = [
            record
            for record in all_records
            if record["car_id"] == car["id"]
        ]

        if car_records:
            latest_record = max(
                car_records,
                key=lambda record: record["sv_mileage"]
            )

            last_service_mileage = latest_record["sv_mileage"]
            service_interval = latest_record["sv_interval"]
            next_service_mileage = (last_service_mileage + service_interval)
            due_in = (next_service_mileage - car["current_mileage"])

            if due_in <= 0:
                status = "🔴 Due / Overdue"
            elif due_in <= 1000:
                status = "🟠 Due Soon"
            else:
                status = "🟢 OK"

            service_types = ", ".join(latest_record["sv_type"])
            service_status.append({
                "Car Plate": car["car_plate"],
                "Car": f"{car['brand']} {car['model']}",
                "Current Mileage": car["current_mileage"],
                "Last Service": last_service_mileage,
                "Service Type": service_types,
                "Interval": service_interval,
                "Next Service": next_service_mileage,
                "Due In": due_in,
                "Status": status
            })

        else:
            service_status.append({
                "Car Plate": car["car_plate"],
                "Car": f"{car['brand']} {car['model']}",
                "Current Mileage": car["current_mileage"],
                "Last Service": "-",
                "Service Type": "-",
                "Interval": "-",
                "Next Service": "-",
                "Due In": "-",
                "Status": "⚪ No Record"
            })

    if service_status:
        dashboard_df = pd.DataFrame(service_status)

        st.dataframe(
            dashboard_df,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No dashboard data available")

def car_assistant_page():
    st.header("🤖 Car Assistant")
    st.write("Ask me anything about cars, maintenance, or your vehicle records.")

    agent = create_chat_agent()  
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_input = st.chat_input("Ask a question about your car...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
        response = agent.invoke({
            "messages": st.session_state.messages
            })
        answer_content = response["messages"][-1].content
        if isinstance(answer_content, list):
            answer = answer_content[0]["text"]
        else:
            answer = answer_content
        st.session_state.messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.write(answer)

def customer_portal_page():
    st.header("👤 Customer Portal")
    st.write("Login to view your vehicle and maintenance information.")

    if "customer_car" not in st.session_state:
        st.session_state.customer_car = None

    if st.session_state.customer_car is None:
        car_plate = st.text_input("Car Plate Number", placeholder="Enter your car plate", autocomplete="off")
        phone = st.text_input("Phone Number", placeholder="Enter your phone number", autocomplete="off")

        if st.button("Login", type="primary"):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/customer/login",
                    json={
                        "car_plate": car_plate,
                        "phone": phone
                    }
                )

                if response.status_code == 200:
                    data = response.json()
                    st.session_state.customer_car = data["car"]
                    st.session_state.customer_messages = []
                    st.success("✅ Login successful!")
                    st.rerun()

                else:
                    error_data = response.json()
                    st.error(f"❌ {error_data.get('detail', 'Login failed')}")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

def customer_car_page():
    car = st.session_state.customer_car

    st.header("🚗 My Car")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Car Plate", car["car_plate"])

    with col2:
        st.metric(
            "Vehicle",
            f"{car['brand']} {car['model']}"
        )

    with col3:
        st.metric(
            "Current Mileage",
            f"{car['current_mileage']:,} km"
        )

    st.write("**Update Current Mileage**")

    new_mileage = st.number_input(
        "Current Mileage (km)",
        min_value=int(car["current_mileage"]),
        value=int(car["current_mileage"]),
        step=100,
        key="customer_update_mileage"
    )

    if st.button("Update Mileage", type="primary"):
        try:
            response = requests.put(
                f"{API_BASE_URL}/customer/mileage",
                json={
                    "car_plate": car["car_plate"],
                    "phone": car["phone"],
                    "current_mileage": new_mileage
                }
            )

            if response.status_code == 200:
                car["current_mileage"] = new_mileage
                st.session_state.customer_car = car
                st.success("✅ Mileage updated successfully!")
                st.rerun()

            else:
                error_data = response.json()
                st.error(
                    f"❌ {error_data.get('detail', 'Failed to update mileage')}"
                )

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

def customer_service_status_page():
    car = st.session_state.customer_car

    st.header("🔔 Service Status")

    car_id = car["_id"]
    maintenance_records, records_success = get_car_maintenance_records(car_id)
    if records_success and maintenance_records:
        latest_record = max(
            maintenance_records,
            key=lambda record: record["sv_mileage"]
        )
        last_service_mileage = latest_record["sv_mileage"]
        service_interval = latest_record["sv_interval"]
        next_service_mileage = last_service_mileage + service_interval
        due_in = next_service_mileage - car["current_mileage"]
        if due_in < 0:
            status_text = "🔴 Overdue"
            due_label = "Overdue By"
            due_display = abs(due_in)
        elif due_in == 0:
            status_text = "🔴 Due Now"
            due_label = "Due In"
            due_display = 0
        elif due_in <= 1000:
            status_text = "🟠 Due Soon"
            due_label = "Due In"
            due_display = due_in
        else:
            status_text = "🟢 OK"
            due_label = "Due In"
            due_display = due_in
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Last Service", f"{last_service_mileage:,} km")
        with col2:
            st.metric("Next Service", f"{next_service_mileage:,} km")
        with col3:
            st.metric(due_label, f"{due_display:,} km")
        with col4:
            st.metric("Status", status_text)
        if latest_record.get("next_service_date"):
            next_date = pd.to_datetime(
                latest_record["next_service_date"]
            ).strftime("%Y-%m-%d")
            st.info(f"📅 Next Service Date: {next_date}")
    else:
        st.info("No maintenance records found.")

def customer_maintenance_history_page():
    car = st.session_state.customer_car

    st.header("📋 Maintenance History")
    car_id = car["_id"]
    maintenance_records, records_success = get_car_maintenance_records(car_id)
    if records_success and maintenance_records:
        history_data = []
        for record in maintenance_records:
            history_data.append({
                "Service Date": pd.to_datetime(
                    record["sv_date"]
                ).strftime("%Y-%m-%d"),
                "Next Service Date": (
                    pd.to_datetime(
                        record["next_service_date"]
                    ).strftime("%Y-%m-%d")
                    if record.get("next_service_date")
                    else "-"
                ),
                "Mileage": f"{record['sv_mileage']:,} km",
                "Service Type": ", ".join(
                    record["sv_type"]
                ),
                "Cost": f"RM {record['cost']:,.2f}",
                "Notes": (
                    record["notes"]
                    if record["notes"]
                    else "-"
                )
            })
        history_df = pd.DataFrame(history_data)
        st.dataframe(history_df, use_container_width=True, hide_index=True)
    else:
        st.info("No maintenance history found.")

def customer_assistant_page():
    car = st.session_state.customer_car

    st.header("🤖 Customer Car Assistant")
    car_id = car["_id"]
    maintenance_records, records_success = get_car_maintenance_records(car_id)
    customer_agent = create_customer_chat_agent()

    if "customer_messages" not in st.session_state:
        st.session_state.customer_messages = []
    for message in st.session_state.customer_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    customer_input = st.chat_input(
        "Ask about your car or general automotive questions..."
    )

    if customer_input:
        st.session_state.customer_messages.append({"role": "user", "content": customer_input})
        with st.chat_message("user"):
            st.write(customer_input)
        vehicle_context = f"""
        CURRENT CUSTOMER VEHICLE:
        Car Plate: {car['car_plate']}
        Brand: {car['brand']}
        Model: {car['model']}
        Year: {car['year']}
        Current Mileage: {car['current_mileage']} km
        """

        if records_success and maintenance_records:
            latest_record = max( maintenance_records, key=lambda record: record["sv_mileage"])
            latest_next_service_date = (latest_record["next_service_date"]
                if latest_record.get("next_service_date")
                else "N/A"
            )
            latest_next_service_mileage = (latest_record["sv_mileage"] + latest_record["sv_interval"])
            due_in = (latest_next_service_mileage - car["current_mileage"])
            vehicle_context += f"""

            LATEST MAINTENANCE RECORD:
            Service Date: {latest_record['sv_date']}
            Next Service Date: {latest_next_service_date}
            Service Mileage: {latest_record['sv_mileage']} km
            Service Interval: {latest_record['sv_interval']} km
            Next Service Mileage: {latest_next_service_mileage} km
            Current Mileage: {car['current_mileage']} km
            Due In: {due_in} km

            IMPORTANT:
            For questions about the customer's current next service date,
            next service mileage, or how many kilometres are left,
            use the LATEST MAINTENANCE RECORD above.
            """            
            vehicle_context += "\nMAINTENANCE HISTORY:\n"
            for record in maintenance_records:
                next_service_date = (
                    record["next_service_date"]
                    if record.get("next_service_date")
                    else "N/A"
                )
                vehicle_context += (
                    f"- Service Date: {record['sv_date']}, "
                    f"Next Service Date: {next_service_date}, "
                    f"Service Type: {', '.join(record['sv_type'])}, "
                    f"Mileage: {record['sv_mileage']} km, "
                    f"Interval: {record['sv_interval']} km, "
                    f"Cost: RM {record['cost']}\n"
                )
        messages = [
            {
                "role": "user",
                "content": f"""
                {vehicle_context}
                Use the vehicle information above when relevant.
                Continue the conversation naturally and use previous messages for context.
                """
            }
        ]

        messages.extend(st.session_state.customer_messages)
        response = customer_agent.invoke({"messages": messages})
        answer_content = response["messages"][-1].content
        if isinstance(answer_content, list):
            answer = answer_content[0]["text"]
        else:
            answer = answer_content
        st.session_state.customer_messages.append({ "role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.write(answer)

if __name__ == "__main__":
    main()












# "name": name,
# "phone": phone,
# "car_plate": car_plate,
# "brand": brand,
# "model": model,
# "year": year,
# "current_mileage": current_mileage,

# sv_type
# sv_date
# sv_mileage
# sv_interval=
# cost
# notes