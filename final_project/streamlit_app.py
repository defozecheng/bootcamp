import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import json

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
                "brand": brand, "model": model, 
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

def create_maintenance_record(car_id, sv_type, sv_date, sv_mileage, sv_interval, cost, notes):
    try:
        response = requests.post(
            f"{API_BASE_URL}/maintenance_records/",
            json={
                "car_id": car_id, 
                "sv_type": sv_type,
                "sv_date": sv_date.isoformat(), 
                "sv_mileage": sv_mileage,
                "sv_interval": sv_interval,
                "cost": cost,
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

def update_maintenance_record(record_id, car_id, sv_type, sv_date, sv_mileage, sv_interval, cost, notes):
    try:
        response = requests.put(
            f"{API_BASE_URL}/maintenance_records/{record_id}",
            json={
                "car_id": car_id,
                "sv_type": sv_type,
                "sv_date": sv_date.isoformat(), 
                "sv_mileage": sv_mileage,
                "sv_interval": sv_interval,
                "cost": cost,
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
    page = st.sidebar.selectbox(
        "Select Page",
        ["🚗 Car", "🛠️ Maintenance Records", "📊 Dashboard"]
    )

    if page == "🚗 Car":
        cars_page()
    elif page == "🛠️ Maintenance Records":
        maintenance_record_page()
    elif page == "📊 Dashboard":
        dashboard_page()

def cars_page():
    st.header("🚗 Car Management")

    tab1, tab2, tab3 = st.tabs(["Add Car","View Cars", "Manage Car"])

    with tab1:
        st.subheader("➕ Add New Car")
        with st.form("create_car_form", clear_on_submit=True):
            col1, col2,col3 = st.columns(3)
            with col1:
                name = st.text_input("Name", placeholder="Enter car owner name")
                phone = st.text_input("Phone Number", placeholder="Enter phone number")
                car_plate = st.text_input("Car Plate Number", placeholder="Enter car plate number")
            with col2:
                brand = st.selectbox("Select Car Brand",["BMW", "BYD", "Chery", "GMW/Haval",
                                        "Honda", "iCaur", "Isuzu", "Jetour", "Leapmotor",
                                        "Lexus", "Mazda", "Mercedes-Benz", "Mitsubishi",
                                        "Nissan", "Omada/Jaecoo", "Perodua", "Proton",
                                        "Tesla", "Toyota", "Zeekr"])
                model = st.text_input("Model", placeholder="Enter car model")
            with col3:
                year = st.number_input("Year", min_value=1950,max_value=2026, value=2025)
                current_mileage = st.number_input("Current Mileage",placeholder=" Enter current mileage", min_value=0, step=1000)

            submitted = st.form_submit_button("Create Car", type="primary")

            if submitted:
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
                        brands = ["BMW", "BYD", "Chery", "GMW/Haval",
                                "Honda", "iCaur", "Isuzu", "Jetour", "Leapmotor",
                                "Lexus", "Mazda", "Mercedes-Benz", "Mitsubishi",
                                "Nissan", "Omada/Jaecoo", "Perodua", "Proton",
                                "Tesla", "Toyota", "Zeekr"]
                        with st.form("update_car_form"):
                            new_name = st.text_input("Name", value=selected_car['name'])
                            new_phone = st.text_input("Phone Number", value=selected_car['phone'])
                            new_car_plate = st.text_input("Car Plate Number", value=selected_car['car_plate'])
                            new_brand = st.selectbox("Select Car Brand", brands, index=brands.index(selected_car['brand']))
                            new_model = st.text_input("Model", value=selected_car['model'])
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
        with st.form("create_record_form", clear_on_submit=True):
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
            sv_mileage = st.number_input("Current Mileage at Service (km)", min_value=0, step=1000,value=int(selected_car["current_mileage"]))
            sv_interval= st.selectbox("Service Interval (km)", [5000,10000,15000,20000])
            next_service_mileage = sv_mileage + sv_interval
            st.info(f"Next Service Mileage: {next_service_mileage:,} km")
            cost = st.number_input("Cost (RM)", min_value=0.0, value=0.0, step=10.0)
            notes = st.text_input("Notes", placeholder="Remarks")

            submitted = st.form_submit_button("Create Maintenance Record", type= "primary")

            if submitted:
                if selected_car_display and sv_type and sv_date:
                    car_id = selected_car_id
                    sv_date_datetime = datetime.combine(sv_date, datetime.min.time())
                    result, record_success = create_maintenance_record(car_id, sv_type, sv_date_datetime, sv_mileage, sv_interval, cost, notes)
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
                            st.write(f"**Service Date:** {maintenance_record['sv_date']}")
                            st.write(f"**Current Mileage at Service:** {maintenance_record['sv_mileage']:,}km")
                            st.write(f"**Service Interval** {maintenance_record['sv_interval']:,}km")
                            next_service_mileage = (maintenance_record["sv_mileage"] + maintenance_record["sv_interval"])
                            st.write(f"**Next Service Mileage:** {next_service_mileage:,} km")
                            st.write(f"**Cost:** RM {maintenance_record['cost']:,.2f}")
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
                        with st.form("update_record_form"):
                            new_sv_type = st.multiselect("Service type", types, default=(selected_record['sv_type']))
                            new_sv_date = st.date_input("Service date", value=pd.to_datetime(selected_record['sv_date']).date())
                            new_sv_mileage = st.number_input("Current Mileage at Service (km)", value=selected_record['sv_mileage'], min_value=0,step=1000)
                            new_sv_interval = st.selectbox("Service Interval (km)", intervals, index=intervals.index(selected_record['sv_interval']))
                            new_next_service_mileage = (new_sv_mileage + new_sv_interval)
                            st.info(f"Next Service Mileage: {new_next_service_mileage:,} km")
                            new_cost = st.number_input("Cost (RM)", min_value=0.0, value=float(selected_record['cost']), step=10.0)
                            new_notes = st.text_input("Notes", value=selected_record['notes'])
                            if st.form_submit_button("Update Record", type="primary"):
                                new_sv_date_datetime = datetime.combine(new_sv_date,datetime.min.time())
                                result, update_success = update_maintenance_record(selected_record_id, car_id, new_sv_type, new_sv_date_datetime, new_sv_mileage, new_sv_interval, new_cost, new_notes)
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
        st.metric( "💰 Total Maintenance Cost", f"RM {total_cost:,.2f}")

    with col4:
        st.metric("📊 Average Service Cost", f"RM {average_cost:,.2f}")

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