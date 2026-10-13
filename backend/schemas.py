

from datetime import datetime
from typing import Literal, Optional

from pydantic import (
BaseModel,
ConfigDict,
EmailStr,
Field,
StringConstraints,
)
from typing_extensions import Annotated

==============================

Common Configuration

==============================

class ORMBase(BaseModel):
model_config = ConfigDict(from_attributes=True)

==============================

Authentication Schemas

==============================

class RegisterIn(BaseModel):
name: str = Field(min_length=2, max_length=120)
email: EmailStr
password: str = Field(min_length=8, max_length=72)

class LoginIn(BaseModel):
email: EmailStr
password: str = Field(min_length=1, max_length=72)

class TokenOut(BaseModel):
access_token: str
token_type: str = "bearer"

class UserOut(ORMBase):
id: int
name: str
email: EmailStr
role: str
is_active: bool

==============================

Event Schemas

==============================

class EventCreate(BaseModel):
name: str = Field(min_length=3, max_length=200)
category: Optional[str] = Field(default=None, max_length=100)
location: Optional[str] = Field(default=None, max_length=200)
description: Optional[str] = None
event_date: datetime
price: float = Field(ge=0)
capacity: int = Field(default=100, gt=0)

class EventOut(ORMBase):
id: int
name: str
category: Optional[str] = None
location: Optional[str] = None
description: Optional[str] = None
event_date: datetime
price: float
capacity: int
created_at: datetime

==============================

Booking Schemas

==============================

class BookingCreate(BaseModel):
event_id: int
quantity: int = Field(default=1, gt=0, le=20)
coupon_code: Optional[str] = Field(default=None, max_length=50)

class BookingOut(ORMBase):
id: int
user_id: int
event_id: int
quantity: int
total_amount: float
coupon_id: Optional[int] = None
discount_amount: float = 0
final_amount: Optional[float] = None
status: str
created_at: datetime

==============================

Payment Schemas

==============================

class PaymentCreateIn(BaseModel):
booking_id: int = Field(gt=0)
payment_method: Literal[
"SIMULATION",
"STRIPE",
"CARD",
"UPI",
"NETBANKING",
]

class PaymentOut(ORMBase):
id: int
booking_id: int
payment_method: str
payment_status: Literal["PENDING", "SUCCESS", "FAILED"]
transaction_id: Optional[str] = None
amount: float
created_at: datetime

class PaymentResult(BaseModel):
payment_id: int
booking_id: int
payment_status: Literal["PENDING", "SUCCESS", "FAILED"]
transaction_id: Optional[str] = None
amount: float
booking_status: str

==============================

Coupon Schemas

==============================

class CouponCreate(BaseModel):
coupon_code: str = Field(
min_length=2,
max_length=50,
pattern=r"^[A-Za-z0-9_-]+$",
)
discount_type: Literal["PERCENTAGE", "FIXED"]
discount_value: float = Field(gt=0)
minimum_booking_amount: float = Field(default=0, ge=0)
expiry_date: datetime
usage_limit: Optional[int] = Field(default=None, gt=0)
is_active: bool = True

class CouponOut(ORMBase):
id: int
coupon_code: str
discount_type: Literal["PERCENTAGE", "FIXED"]
discount_value: float
minimum_booking_amount: float
expiry_date: datetime
usage_limit: Optional[int] = None
usage_count: int
is_active: bool
created_at: datetime

class CouponValidateIn(BaseModel):
coupon_code: str = Field(min_length=2, max_length=50)
booking_amount: float = Field(gt=0)

class CouponValidationOut(BaseModel):
coupon_id: int
coupon_code: str
discount_amount: float
final_amount: float

==============================

Review Schemas

==============================

class ReviewCreateIn(BaseModel):
event_id: int = Field(gt=0)
rating: int = Field(ge=1, le=5)
review_text: Optional[str] = Field(
default=None,
max_length=2000,
)

class ReviewUpdate(BaseModel):
rating: Optional[int] = Field(default=None, ge=1, le=5)
review_text: Optional[str] = Field(
default=None,
max_length=2000,
)

class ReviewOut(ORMBase):
id: int
user_id: int
event_id: int
rating: int
review_text: Optional[str] = None
created_at: datetime

class ReviewListOut(BaseModel):
event_id: int
average_rating: Optional[float] = None
count: int
reviews: list[ReviewOut]

==============================

Notification Schemas

==============================

class NotificationCreate(BaseModel):
user_id: int = Field(gt=0)
title: str = Field(min_length=1, max_length=200)
message: str = Field(min_length=1)
notification_type: Literal[
"EVENT",
"BOOKING",
"PAYMENT",
"SYSTEM",
] = "SYSTEM"

class NotificationOut(ORMBase):
id: int
user_id: int
title: str
message: str
notification_type: Literal[
"EVENT",
"BOOKING",
"PAYMENT",
"SYSTEM",
]
is_read: bool
created_at: datetime

class NotificationReadResponse(BaseModel):
message: str
