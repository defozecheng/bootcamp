
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List
from datetime import datetime
from bson.objectid import ObjectId
from database import DatabaseManager
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="MongoDB Database API", version="1.0.0")

class CarCreate(BaseModel):
    name: str
    phone: str
    car_plate: str
    brand: str
    model: str
    year: int
    current_mileage: int

class CustomerLogin(BaseModel):
    car_plate: str
    phone: str

class CustomerMileageUpdate(BaseModel):
    car_plate: str
    phone: str
    current_mileage: int

class CarResponse(BaseModel):
    id: str
    name: str
    phone: str
    car_plate: str
    brand: str
    model: str
    year: int
    current_mileage: int
    created_at: datetime

class MaintenanceRecordCreate(BaseModel):
    car_id: str
    sv_type: List[str]
    sv_date: datetime
    sv_mileage: int
    sv_interval: int
    cost: float
    notes: str

class MaintenanceRecordResponse(BaseModel):
    record_id:str
    car_id: str
    sv_type: List[str]
    sv_date: datetime
    sv_mileage: int
    sv_interval: int
    cost: float
    notes: str
    created_at: datetime

try:
    db = DatabaseManager()
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    db = None

@app.get("/")
async def root():
    return {"message": "MongoDB API", "version": "1.0.0"}

# Car API

@app.post("/customer/login")
async def customer_login(customer: CustomerLogin):
    try:
        car = db.get_car_by_customer(customer.car_plate, customer.phone)
        if not car:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid car plate or phone number."
            )

        return {"message": "Login successful", "car": car}

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@app.put("/customer/mileage")
async def update_customer_mileage(customer: CustomerMileageUpdate):
    try:
        car = db.get_car_by_customer(customer.car_plate, customer.phone)

        if not car:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid car plate or phone number."
            )
        if customer.current_mileage < car["current_mileage"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New mileage cannot be lower than current mileage."
            )
        
        success = db.update_car_mileage(car["_id"], customer.current_mileage)
        if success:
            return {
                "message": "Mileage updated successfully",
                "current_mileage": customer.current_mileage
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mileage was not updated."
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@app.post("/cars/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_car(car: CarCreate):
    try:
        car_id = db.create_car(car.name, car.phone, car.car_plate, car.brand, car.model, car.year, car.current_mileage)
        if car_id:
            return {"message": "Car created successfully", "car_id": car_id}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="failed to create car. Car plate might already exist."
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/cars/", response_model=List[CarResponse])
async def get_all_cars():
    try:
        cars = db.get_all_cars()
        return[
            CarResponse(
                id=car['_id'],
                name=car['name'],
                phone=car['phone'],
                car_plate=car['car_plate'],
                brand=car['brand'],
                model=car['model'],
                year=car['year'],
                current_mileage=car['current_mileage'],
                created_at=car['created_at']
            )
            for car in cars
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= f"Internal server error: {str(e)}"
        )

@app.get("/cars/{car_id}", response_model=CarResponse)
async def get_car(car_id: str):
    try:
        if not ObjectId.is_valid(car_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid car ID format"
            )

        car = db.get_car(car_id)

        if not car:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Car not found"
            )

        return CarResponse(
            id=car['_id'],
            name=car['name'],
            phone=car['phone'],
            car_plate=car['car_plate'],
            brand=car['brand'],
            model=car['model'],
            year=car['year'],
            current_mileage=car['current_mileage'],
            created_at=car['created_at']
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@app.put("/cars/{car_id}", response_model=dict)
async def update_car(car_id: str, car_update: CarCreate):
    try:
        if not ObjectId.is_valid(car_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid car ID format"
            )
        existing_car = db.get_car(car_id)
        if not existing_car:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Car not found"
            )
        result = db.update_car(
                car_id,
                car_update.name,
                car_update.phone, 
                car_update.car_plate,
                car_update.brand,
                car_update.model,
                car_update.year,
                car_update.current_mileage
        )
        if result:
            return {"message": "Car updated successfully"}
        else:
            return {"message": "No changes made to car"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@app.delete("/cars/{car_id}", response_model=dict)
async def delete_car(car_id: str):
    try:
        if not ObjectId.is_valid(car_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid car ID format"
            )
        car = db.get_car(car_id)
        if not car:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Car not found"
            )
        success = db.delete_car(car_id)
        if success:
            return {"message": "Car deleted successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to delete car"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
    
# Maintenance API

@app.post("/maintenance_records/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_maintenance_record(maintenance_record: MaintenanceRecordCreate):
    try:
        if not ObjectId.is_valid(maintenance_record.car_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid car ID format"
            )
        car =  db.get_car(maintenance_record.car_id)
        if not car:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Car not found"
            )
        record_id = db.create_maintenance_record(
            maintenance_record.car_id,
            maintenance_record.sv_type,
            maintenance_record.sv_date,
            maintenance_record.sv_mileage,
            maintenance_record.sv_interval,
            maintenance_record.cost,
            maintenance_record.notes
        )
        if record_id:
            if maintenance_record.sv_mileage > car["current_mileage"]:
                db.update_car_mileage(maintenance_record.car_id, maintenance_record.sv_mileage)
            return{"message": "Record created successfully", "record_id": record_id}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create record"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/cars/{car_id}/maintenance_records", response_model=List[MaintenanceRecordResponse])
async def get_car_maintenance_records(car_id: str):
    try:
        if not ObjectId.is_valid(car_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid car ID format"
            )

        car = db.get_car(car_id)

        if not car:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Car not found"
            )
        
        maintenance_records = db.get_car_maintenance_records(car_id)
        return [
            MaintenanceRecordResponse(
                record_id=maintenance_record['_id'],
                car_id=maintenance_record["car_id"],
                sv_type=maintenance_record['sv_type'],
                sv_date=maintenance_record['sv_date'],
                sv_mileage=maintenance_record['sv_mileage'],
                sv_interval=maintenance_record['sv_interval'],
                cost=maintenance_record['cost'],
                notes=maintenance_record['notes'],
                created_at=maintenance_record["created_at"]
            )
            for maintenance_record in maintenance_records
        ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/maintenance_records/{record_id}", response_model=MaintenanceRecordResponse)
async def get_maintenance_record(record_id: str):
    try:
        if not ObjectId.is_valid(record_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid record ID format"
            )

        maintenance_record = db.get_maintenance_record(record_id)
        if not maintenance_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Maintenance record not found"
            )
        return MaintenanceRecordResponse(
                record_id=maintenance_record['_id'],
                car_id=maintenance_record["car_id"],
                sv_type=maintenance_record['sv_type'],
                sv_date=maintenance_record['sv_date'],
                sv_mileage=maintenance_record['sv_mileage'],
                sv_interval=maintenance_record['sv_interval'],
                cost=maintenance_record['cost'],
                notes=maintenance_record['notes'],
                created_at=maintenance_record["created_at"]
            )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@app.put("/maintenance_records/{record_id}", response_model=dict)
async def update_maintenance_record(record_id: str, maintenance_record_update: MaintenanceRecordCreate):
    try:
        if not ObjectId.is_valid(record_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid record ID format"
            )
        existing_record = db.get_maintenance_record(record_id)
        if not existing_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Maintenance record not found"
            )
        result = db.update_maintenance_record(
                record_id,
                maintenance_record_update.sv_type, 
                maintenance_record_update.sv_date,
                maintenance_record_update.sv_mileage,
                maintenance_record_update.sv_interval,
                maintenance_record_update.cost,
                maintenance_record_update.notes
        )
        if result:
            return {"message": "Maintenance record updated successfully"}
        else:
            return {"message": "No changes made to maintenance record"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@app.delete("/maintenance_records/{record_id}", response_model=dict)
async def delete_maintenance_record(record_id: str):
    try:
        if not ObjectId.is_valid(record_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid record ID format"
            )
        maintenance_record = db.get_maintenance_record(record_id)
        if not maintenance_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Maintenance record not found"
            )
        success = db.delete_maintenance_record(record_id)
        if success:
            return {"message": "Maintenance record deleted successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to delete maintenance record"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )





