

from datetime import datetime

from sqlalchemy import (
Boolean,
Column,
DateTime,
Float,
ForeignKey,
Integer,
String,
Text,
UniqueConstraint,
)
from sqlalchemy.orm import relationship

from database import Base

==============================

User Model

==============================

class User(Base):
tablename = "users"

id = Column(Integer, primary_key=True, index=True)
name = Column(String(120), nullable=False)
email = Column(String(255), unique=True, index=True, nullable=False)
password_hash = Column(String(255), nullable=False)
role = Column(String(30), default="user", nullable=False)
is_active = Column(Boolean, default=True, nullable=False)

bookings = relationship("Booking", back_populates="user")
reviews = relationship("Review", back_populates="user")
notifications = relationship(
    "Notification", back_populates="user"
)

==============================

Event Model

==============================

class Event(Base):
tablename = "events"

id = Column(Integer, primary_key=True, index=True)
name = Column(String(200), nullable=False, index=True)
category = Column(String(100), nullable=True, index=True)
location = Column(String(200), nullable=True, index=True)
description = Column(Text, nullable=True)
event_date = Column(DateTime, nullable=False, index=True)
price = Column(Float, default=0.0, nullable=False)
capacity = Column(Integer, default=100, nullable=False)
created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

bookings = relationship("Booking", back_populates="event")
reviews = relationship("Review", back_populates="event")

==============================

Coupon Model

==============================

class Coupon(Base):
tablename = "coupons"

id = Column(Integer, primary_key=True, index=True)
coupon_code = Column(
    String(50), unique=True, index=True, nullable=False
)
discount_type = Column(String(20), nullable=False)
discount_value = Column(Float, nullable=False)
minimum_booking_amount = Column(Float, default=0.0, nullable=False)
expiry_date = Column(DateTime, nullable=False)
usage_limit = Column(Integer, nullable=True)
usage_count = Column(Integer, default=0, nullable=False)
is_active = Column(Boolean, default=True, nullable=False)
created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

bookings = relationship("Booking", back_populates="coupon")

==============================

Booking Model

==============================

class Booking(Base):
tablename = "bookings"

id = Column(Integer, primary_key=True, index=True)
user_id = Column(
    Integer, ForeignKey("users.id"), nullable=False, index=True
)
event_id = Column(
    Integer, ForeignKey("events.id"), nullable=False, index=True
)

quantity = Column(Integer, default=1, nullable=False)
total_amount = Column(Float, nullable=False)

coupon_id = Column(
    Integer, ForeignKey("coupons.id"), nullable=True
)
discount_amount = Column(Float, default=0.0, nullable=False)
final_amount = Column(Float, nullable=True)

status = Column(String(30), default="PENDING", nullable=False)
created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

user = relationship("User", back_populates="bookings")
event = relationship("Event", back_populates="bookings")
coupon = relationship("Coupon", back_populates="bookings")
payments = relationship("Payment", back_populates="booking")

==============================

Payment Model

==============================

class Payment(Base):
tablename = "payments"

id = Column(Integer, primary_key=True, index=True)
booking_id = Column(
    Integer, ForeignKey("bookings.id"), nullable=False, index=True
)

payment_method = Column(String(40), nullable=False)
payment_status = Column(
    String(20), default="PENDING", nullable=False
)
transaction_id = Column(
    String(120), unique=True, nullable=True
)
amount = Column(Float, nullable=False)
created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

booking = relationship("Booking", back_populates="payments")

==============================

Review Model

==============================

class Review(Base):
tablename = "reviews"

__table_args__ = (
    UniqueConstraint(
        "user_id", "event_id", name="uq_review_user_event"
    ),
)

id = Column(Integer, primary_key=True, index=True)
user_id = Column(
    Integer, ForeignKey("users.id"), nullable=False, index=True
)
event_id = Column(
    Integer, ForeignKey("events.id"), nullable=False, index=True
)
rating = Column(Integer, nullable=False)
review_text = Column(Text, nullable=True)
created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

user = relationship("User", back_populates="reviews")
event = relationship("Event", back_populates="reviews")

==============================

Notification Model

==============================

class Notification(Base):
tablename = "notifications"

id = Column(Integer, primary_key=True, index=True)
user_id = Column(
    Integer, ForeignKey("users.id"), nullable=False, index=True
)
title = Column(String(200), nullable=False)
message = Column(Text, nullable=False)
notification_type = Column(
    String(20), default="SYSTEM", nullable=False
)
is_read = Column(Boolean, default=False, nullable=False)
created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

user = relationship("User", back_populates="notifications")
