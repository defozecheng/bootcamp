
from fastapi import FastAPI, HTTPException, status
from contextlib import asynccontextmanager
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from bson.objectid import ObjectId
from database import DatabaseManager
import os
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
    sv_type: str
    sv_date: datetime
    sv_mileage: int
    sv_interval: int
    cost: float
    notes: str

class MaintenanceRecordResponse(BaseModel):
    id:str
    car_id: str
    sv_type: str
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

@app.post("/cars/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_car(car: CarCreate):
    try:
        car_id = db.create_car(car.name, car.phone, car.car_plate, car.brand, car.model, car.year, car.current_mileage)
        if car_id:
            return {"message": "Car created successufully", "car_id": car_id}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="failed to create car. Car plate might already exist."
            )
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

#     car_id: str
#     sv_type: str
#     sv_date: datetime
#     sv_mileage: int
#     sv_interval: int
#     cost: float
#     notes: str

