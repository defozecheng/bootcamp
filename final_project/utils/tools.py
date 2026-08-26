import os
from langchain_core.tools import tool
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

@tool
def get_car_data(car_plate: str) -> str:
    """
    Fetch car and maintenance information from the database.

    Use this tool when the user asks about:
    - Cars stored in the database
    - Car details
    - Current mileage
    - Maintenance history
    - Service records
    - Car plate, brand, model, or year

    Args:
        car_plate: The car plate number

    Returns:
        Car and maintenance information from the database
    """

    client = None

    try:
        client = MongoClient(os.getenv("MONGODB_ATLAS_CLUSTER_URI"))
        db = client["car_maintenance_db"]
        cars_collection = db["cars"]
        car = cars_collection.find_one({"car_plate": car_plate.upper()})
        if not car:
            return f"No car found with plate {car_plate}."

        return (
                f"Car Plate: {car.get('car_plate', 'N/A')}, "
                f"Brand: {car.get('brand', 'N/A')}, "
                f"Model: {car.get('model', 'N/A')}, "
                f"Year: {car.get('year', 'N/A')}, "
                f"Current Mileage: {car.get('current_mileage', 'N/A')} km"
            )
    
    except Exception as e:
        return f"Error fetching data: {str(e)}"

    finally:
        if client:
            client.close()

@tool
def get_maintenance_history(car_plate: str) -> str:
    """
    Fetch maintenance history for a specific car.

    Use this tool when the user asks about:
    - Maintenance history
    - Previous service records
    - Service types performed
    - Service mileage
    - Service interval
    - Next service mileage
    - Maintenance cost

    Args:
        car_plate: The car plate number, for example W123W

    Returns:
        Maintenance records for the selected car.
    """

    client = None

    try:
        client = MongoClient(os.getenv("MONGODB_ATLAS_CLUSTER_URI"))
        db = client["car_maintenance_db"]
        cars_collection = db["cars"]
        maintenance_collection = db["maintenance_records"]
        car = cars_collection.find_one({
            "car_plate": car_plate.upper()
        })
        if not car:
            return f"No car found with plate {car_plate}."

        car_id = car["_id"]
        records = list(maintenance_collection.find({"car_id": car_id}).sort("sv_mileage", -1))

        if not records:
            return f"No maintenance records found for {car_plate}."
        result = []
        for record in records:
            next_service_mileage = (record.get("sv_mileage", 0) + record.get("sv_interval", 0))

            record_info = (
                f"Service Type: {record.get('sv_type', 'N/A')}, "
                f"Service Date: {record.get('sv_date', 'N/A')}, "
                f"Next Service Date: {record.get('next_service_date', 'N/A')}, "
                f"Mileage at Service: {record.get('sv_mileage', 'N/A')} km, "
                f"Service Interval: {record.get('sv_interval', 'N/A')} km, "
                f"Next Service Mileage: {next_service_mileage} km, "
                f"Cost: RM {record.get('cost', 'N/A')}, "
                f"Notes: {record.get('notes', 'N/A')}"
            )
            result.append(record_info)
        return "\n".join(result)
    except Exception as e:
        return f"Error fetching maintenance history: {str(e)}"

    finally:
        if client:
            client.close()

tools = [get_car_data,get_maintenance_history]