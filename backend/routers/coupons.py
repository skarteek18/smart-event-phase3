
# Find coupon
coupon = (
    db.query(Coupon)
    .filter(Coupon.coupon_code == coupon_code)
    .first()
)

if not coupon:
    raise HTTPException(
        status_code=404,
        detail="Coupon not found",
    )

# Check whether coupon is active
if not coupon.is_active:
    raise HTTPException(
        status_code=400,
        detail="Coupon is inactive",
    )

# Check expiration date
expiry = coupon.expiry_date
now = datetime.now(timezone.utc)

# Support existing SQLite datetimes that may be timezone-naive
if expiry.tzinfo is None:
    now = now.replace(tzinfo=None)

if expiry < now:
    raise HTTPException(
        status_code=400,
        detail="Coupon has expired",
    )

# Check usage limit
if (
    coupon.usage_limit is not None
    and coupon.usage_count >= coupon.usage_limit
):
    raise HTTPException(
        status_code=400,
        detail="Coupon usage limit has been reached",
    )

# Check minimum booking amount
booking_amount = payload.booking_amount

if booking_amount < coupon.minimum_booking_amount:
    raise HTTPException(
        status_code=400,
        detail=(
            "Minimum booking amount required is "
            f"{coupon.minimum_booking_amount:.2f}"
        ),
    )

# Calculate discount
if coupon.discount_type == "PERCENTAGE":
    if coupon.discount_value > 100:
        raise HTTPException(
            status_code=400,
            detail="Percentage discount cannot exceed 100",
        )

    discount_amount = (
        booking_amount * coupon.discount_value / 100
    )

elif coupon.discount_type == "FIXED":
    discount_amount = coupon.discount_value

else:
    raise HTTPException(
        status_code=400,
        detail="Invalid coupon discount type",
    )

# Discount cannot exceed booking total
discount_amount = min(
    booking_amount,
    max(0, discount_amount),
)

final_amount = booking_amount - discount_amount

return {
    "message": "Coupon applied successfully",
    "coupon_id": coupon.id,
    "coupon_code": coupon.coupon_code,
    "discount_type": coupon.discount_type,
    "discount_value": coupon.discount_value,
    "booking_amount": round(booking_amount, 2),
    "discount_amount": round(discount_amount, 2),
    "final_amount": round(final_amount, 2),
}
