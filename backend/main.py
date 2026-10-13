
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import User
from schemas import RegisterIn, LoginIn, TokenOut
from security import hash_password, verify_password, create_access_token

from routers import (
payments,
coupons,
reviews,
notifications,
events,
)

Initialize database tables

Base.metadata.create_all(bind=engine)

Initialize FastAPI application

app = FastAPI(
title="SmartEvent API",
description=(
"SmartEvent Phase 3: Event Payments, Coupons, "
"Reviews, Notifications, Search and Filtering."
),
version="3.0.0",
)

Configure CORS for React frontend

app.add_middleware(
CORSMiddleware,
allow_origins=[
"http://localhost:5173",
"http://127.0.0.1:5173",
],
allow_credentials=True,
allow_methods=[""],
allow_headers=[""],
)

Register API routers

app.include_router(payments.router)
app.include_router(coupons.router)
app.include_router(reviews.router)
app.include_router(notifications.router)
app.include_router(events.router)

@app.get("/", tags=["Health"])
def home():
return {
"message": "Welcome to SmartEvent API",
"version": "3.0.0",
"status": "running",
"documentation": "/docs",
}

@app.get("/health", tags=["Health"])
def health_check():
return {"status": "healthy"}

User Registration

@app.post("/auth/register", status_code=201, tags=["Authentication"])
def register(
payload: RegisterIn,
db: Session = Depends(get_db),
):
email = str(payload.email).lower()

existing_user = (
    db.query(User)
    .filter(User.email == email)
    .first()
)

if existing_user:
    raise HTTPException(
        status_code=409,
        detail="Email is already registered",
    )

user = User(
    name=payload.name.strip(),
    email=email,
    password_hash=hash_password(payload.password),
    role="user",
)

db.add(user)
db.commit()
db.refresh(user)

return {
    "message": "Registration successful",
    "user_id": user.id,
    "name": user.name,
    "email": user.email,
}

User Login

@app.post(
"/auth/login",
response_model=TokenOut,
tags=["Authentication"],
)
def login(
payload: LoginIn,
db: Session = Depends(get_db),
):
email = str(payload.email).lower()

user = (
    db.query(User)
    .filter(User.email == email)
    .first()
)

if not user or not verify_password(
    payload.password,
    user.password_hash,
):
    raise HTTPException(
        status_code=401,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

if not user.is_active:
    raise HTTPException(
        status_code=403,
        detail="User account is inactive",
    )

access_token = create_access_token(user.id)

return {
    "access_token": access_token,
    "token_type": "bearer",
}
