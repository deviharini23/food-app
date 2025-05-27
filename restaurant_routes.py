from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Restaurant, User
from geopy.distance import geodesic

router = APIRouter()

# ✅ Optional: Seed restaurant data (run only once)
def seed_restaurants(db: Session):
    if db.query(Restaurant).count() > 0:
        return  # Already seeded

    sample_restaurants = [
        Restaurant(name="Spicy Garden", latitude=12.9718, longitude=77.5937),
        Restaurant(name="The Pizza Hub", latitude=12.9721, longitude=77.5942),
        Restaurant(name="Curry Point", latitude=12.9705, longitude=77.5921),
        Restaurant(name="Burger World", latitude=12.9750, longitude=77.5965),
        Restaurant(name="Tandoori Nights", latitude=12.9695, longitude=77.5910),
    ]
    db.add_all(sample_restaurants)
    db.commit()


@router.on_event("startup")
def startup_event():
    # Seed sample restaurants when app starts
    with next(get_db()) as db:
        seed_restaurants(db)


@router.get("/assign-nearest-restaurant", response_model=dict)
def assign_nearest_restaurant(
    user_id: int = Query(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user or user.latitude is None or user.longitude is None:
        raise HTTPException(status_code=400, detail="User location not found")

    user_location = (user.latitude, user.longitude)

    restaurants = db.query(Restaurant).all()
    if not restaurants:
        raise HTTPException(status_code=404, detail="No restaurants found")

    closest = None
    min_distance = float("inf")

    for r in restaurants:
        distance_km = geodesic(user_location, (r.latitude, r.longitude)).km
        if distance_km < min_distance:
            min_distance = distance_km
            closest = {
                "id": r.id,
                "name": r.name,
                "latitude": r.latitude,
                "longitude": r.longitude,
                "distance_km": round(distance_km, 2)
            }

    if min_distance > 5:
        raise HTTPException(status_code=404, detail="No nearby restaurants within 5 km")

    return closest
