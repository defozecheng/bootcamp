from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
from bson.objectid import ObjectId
import os

load_dotenv()

mongo_uri = os.getenv('MONGODB_ATLAS_CLUSTER_URI')

def normalize_phone(phone):
    phone = phone.replace(" ", "").replace("-", "")

    if phone.startswith("+60"):
        phone = phone[1:]
    elif phone.startswith("0"):
        phone = "60" + phone[1:]

    return phone

class DatabaseManager:
    def __init__(self, db_name='car_maintenance_db', connection_string=mongo_uri):
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]
        self.cars_collection = self.db.cars
        self.maintenance_records_collection = self.db.maintenance_records
        self.init_database()

    def init_database(self):
        self.cars_collection.create_index("car_plate", unique=True)
        self.maintenance_records_collection.create_index("car_id")


# Car function

    def get_car_by_customer(self, car_plate, phone):
        try:
            car = self.cars_collection.find_one({"car_plate": car_plate.upper()})
            if not car:
                return None

            database_phone = normalize_phone(car["phone"])
            customer_phone = normalize_phone(phone)

            if database_phone != customer_phone:
                return None

            car["_id"] = str(car["_id"])
            return car

        except Exception as e:
            print(f"Error verifying customer: {e}")
            return None        

    def create_car(self, name, phone, car_plate, brand, model, year, current_mileage):
        try:
            car_doc = {
                "name": name,
                "phone": phone,
                "car_plate": car_plate,
                "brand": brand,
                "model": model,
                "year": year,
                "current_mileage": current_mileage,
                "created_at": datetime.now()
            }
            result = self.cars_collection.insert_one(car_doc)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_all_cars(self):
        try:
            cars = list(self.cars_collection.find())
            for car in cars:
                car['_id'] = str(car['_id'])
            return cars
        except Exception as e:
            print(f"Error fetching cars: {e}")
            return []

    def get_car(self, car_id):
        try:
            if ObjectId.is_valid(car_id):
                car_object_id = ObjectId(car_id)
            else:
                car_object_id = car_id
            car = self.cars_collection.find_one(
                {"_id": car_object_id}
            )

            if car:
                car["_id"] = str(car["_id"])

            return car
        except Exception as e:
            print(f"Error fetching car: {e}")
            return None

    def update_car(self, car_id, name, phone, car_plate, brand, model, year, current_mileage):
        try:
            if ObjectId.is_valid(car_id):
                car_object_id = ObjectId(car_id)
            else:
                car_object_id = car_id

            update_data = {
                "name": name, 
                "phone": phone, 
                "car_plate": car_plate, 
                "brand": brand, 
                "model": model, 
                "year": year, 
                "current_mileage": current_mileage,
                "updated_at": datetime.now()
                }
            
            result = self.cars_collection.update_one(
                {"_id": car_object_id},
                {"$set": update_data}
                )

            return result.modified_count > 0
        except Exception as e:
            print(f"Error update car: {e}")
            return False
        
    def delete_car(self, car_id):
        try:
            if ObjectId.is_valid(car_id):
                car_object_id = ObjectId(car_id)
            else:
                car_object_id = car_id

            self.maintenance_records_collection.delete_many({"car_id": car_object_id})
            result = self.cars_collection.delete_one({"_id": car_object_id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting car: {e}")
            return False


# Maintenance record function

    def create_maintenance_record(self, car_id, sv_type, sv_date,next_service_date, sv_mileage, sv_interval, cost, paid_amount, notes):
        try:
            if ObjectId.is_valid(car_id):
                car_object_id = ObjectId(car_id)
            else:
                car_object_id = car_id

            maintenance_record_doc = {
                "car_id": car_object_id,
                "sv_type": sv_type,
                "sv_date": sv_date,
                "next_service_date": next_service_date,
                "sv_mileage": sv_mileage,
                "sv_interval": sv_interval,
                "cost": cost,
                "paid_amount": paid_amount,
                "notes": notes,
                "created_at": datetime.now()
            }
            result = self.maintenance_records_collection.insert_one(maintenance_record_doc)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error creating maintenance records: {e}")
            return None

    def get_car_maintenance_records(self, car_id):
        try:
            if ObjectId.is_valid(car_id):
                car_object_id = ObjectId(car_id)
            else:
                car_object_id = car_id

            maintenance_records = list(self.maintenance_records_collection.find(
                {"car_id": car_object_id}
            ).sort("created_at", -1))

            for maintenance_record in maintenance_records:
                maintenance_record['_id'] = str(maintenance_record['_id'])
                maintenance_record["car_id"] = str(maintenance_record['car_id'])
            return maintenance_records
        except Exception as e:
            print(f"Error fetching maintenance records: {e}")
            return []

    def get_maintenance_record(self, record_id):
        try:
            if ObjectId.is_valid(record_id):
                maintenance_record_object_id = ObjectId(record_id)
            else:
                maintenance_record_object_id = record_id
            maintenance_record = self.maintenance_records_collection.find_one(
                {"_id": maintenance_record_object_id}
            )

            if maintenance_record:
                maintenance_record["_id"] = str(maintenance_record["_id"])
                maintenance_record["car_id"] = str(maintenance_record["car_id"])

            return maintenance_record
        except Exception as e:
            print(f"Error fetching maintenance record: {e}")
            return None

    def update_maintenance_record(self, record_id, sv_type, sv_date, next_service_date, sv_mileage, sv_interval, cost, paid_amount, notes):
        try:
            if ObjectId.is_valid(record_id):
                maintenance_record_object_id = ObjectId(record_id)
            else:
                maintenance_record_object_id = record_id

            update_record = {
                "sv_type": sv_type,
                "sv_date": sv_date,
                "next_service_date": next_service_date,
                "sv_mileage": sv_mileage,
                "sv_interval": sv_interval,
                "cost": cost,
                "paid_amount": paid_amount,
                "notes": notes,
                "updated_at": datetime.now()
                }

            result = self.maintenance_records_collection.update_one(
                {"_id": maintenance_record_object_id},
                {"$set": update_record}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error update record: {e}")
            return False

    def update_car_mileage(self, car_id, current_mileage):
        result = self.cars_collection.update_one(
            {"_id": ObjectId(car_id)},
            {"$set": {"current_mileage": current_mileage}}
        )
        return result.modified_count > 0

    def delete_maintenance_record(self, record_id):
        try:
            if ObjectId.is_valid(record_id):
                maintenance_record_object_id = ObjectId(record_id)
            else:
                maintenance_record_object_id = record_id

            result = self.maintenance_records_collection.delete_one({"_id": maintenance_record_object_id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting record: {e}")
            return False

    def close_connection(self):
        self.client.close()



        

    
