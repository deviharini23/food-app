from fastapi import FastAPI, File, UploadFile, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from whisper_handler import transcribe
from chatbot import suggest_dish
from database import get_db, Base, engine, SessionLocal
from models import User, Restaurant, Order
from pydantic import BaseModel
import spacy
import os

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize DB tables
Base.metadata.create_all(bind=engine)

# FastAPI instance
app = FastAPI()

# ✅ Include restaurant router
from restaurant_routes import router as restaurant_router
app.include_router(restaurant_router)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Extract location from text using spaCy
def extract_location(text: str) -> str:
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "GPE":
            return ent.text
    return "Unknown"

# ✅ Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Food Delivery API!"}

@app.get("/favicon.ico")
async def favicon():
    return {}

# ✅ Upload and process voice command
@app.post("/upload-audio/")
async def handle_audio(
    user_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    path = f"temp_{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())

    try:
        text = transcribe(path)
        suggestion = suggest_dish(text)
        location = extract_location(text)

        new_order = Order(user_id=user_id, dish_name=suggestion, location=location)
        db.add(new_order)
        db.commit()

        return {
            "order_text": text,
            "suggestion": suggestion,
            "location": location
        }
    finally:
        if os.path.exists(path):
            os.remove(path)

# ✅ Register user
@app.post("/register/")
def register_user(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(username=username, password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered", "user_id": new_user.id}

# ✅ Login or Register
class UserRequest(BaseModel):
    username: str
    password: str

@app.post("/register_or_login")
def register_or_login(user: UserRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()

    if existing_user:
        if existing_user.password != user.password:
            raise HTTPException(status_code=400, detail="Incorrect password")
        return {"message": "User logged in", "user_id": existing_user.id}

    new_user = User(username=user.username, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered", "user_id": new_user.id}

# ✅ Get order history
@app.get("/orders/{user_id}")
def get_orders(user_id: int, db: Session = Depends(get_db)):
    return db.query(Order).filter(Order.user_id == user_id).all()

# ✅ Live location update
class LocationUpdate(BaseModel):
    user_id: int
    latitude: float
    longitude: float

@app.post("/update_location")
def update_location(location: LocationUpdate):
    db: Session = SessionLocal()
    user = db.query(User).filter(User.id == location.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.latitude = location.latitude
    user.longitude = location.longitude
    db.commit()
    return {"message": "Location updated"}
