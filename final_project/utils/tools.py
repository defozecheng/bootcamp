import os
from langchain_core.tools import tool
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

@tool
def get_car_data(query: str) -> str:
    """
    Fetch car maintenance information from the car service database.

    ONLY use this tool when the user asks about:
    - Cars stored in the database
    - Maintenance records
    - Current mileage at service
    - Service history
    - Service interval
    - Next service mileage
    - Maintenance cost

    DO NOT use this tool for:
    - General automotive knowledge
    - Questions about engines or car parts
    - Greetings or casual conversation

    Args:
        query: The user's question about car or maintenance data

    Returns:
        Maintenance information from the database or an error message
    """

    client = None

    try:
        client = MongoClient(os.getenv("MONGODB_ATLAS_CLUSTER_URI"))
        db = client["car_maintenance_db"]
        collection = db["maintenance_records"]

        maintenance_records = list(collection.find({}).limit(5))

        if maintenance_records:
            result = []

            for maintenance_record in maintenance_records:

                next_service_mileage = (maintenance_record.get("sv_mileage", 0) + maintenance_record.get("sv_interval", 0))

                maintenance_record_info = (
                    f"Service Type: {maintenance_record.get('sv_type', 'N/A')}, "
                    f"Service Date: {maintenance_record.get('sv_date', 'N/A')}, "
                    f"Current Mileage at Service: {maintenance_record.get('sv_mileage', 'N/A')} km, "
                    f"Service Interval: {maintenance_record.get('sv_interval', 'N/A')} km, "
                    f"Next Service Mileage: {next_service_mileage} km, "
                    f"Cost: RM {maintenance_record.get('cost', 'N/A')}, "
                    f"Notes: {maintenance_record.get('notes', 'N/A')}"
                )
                result.append(maintenance_record_info)
            return "\n".join(result)
        else:
            return "No maintenance records in the database."
    except Exception as e:
        return f"Error fetching data: {str(e)}"
    finally:
        if client:
            client.close()


tools = [get_car_data]