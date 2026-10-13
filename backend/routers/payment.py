

if not booking:
    raise HTTPException(
        status_code=404,
        detail="Booking not found",
    )

if booking.status == "CONFIRMED":
    raise HTTPException(
        status_code=400,
        detail="Booking is already confirmed",
    )

if booking.status == "CANCELLED":
    raise HTTPException(
        status_code=400,
        detail="Cannot pay for a cancelled booking",
    )

# Use the discounted amount when available
amount = (
    booking.final_amount
    if booking.final_amount is not None
    else booking.total_amount
)

if amount <= 0:
    raise HTTPException(
        status_code=400,
        detail="Payment amount must be greater than zero",
    )

payment = Payment(
    booking_id=booking.id,
    payment_method=payload.payment_method,
    payment_status="PENDING",
    amount=amount,
)

try:
    db.add(payment)
    db.flush()

    # Development-only payment simulation.
    # Replace this section with a verified payment gateway flow.
    payment.payment_status = "SUCCESS"
    payment.transaction_id = (
        f"SIM-{uuid4().hex[:16].upper()}"
    )

    booking.status = "CONFIRMED"

    notification = Notification(
        user_id=current_user.id,
        title="Payment successful",
        message=(
            f"Payment for booking #{booking.id} "
            "was successful."
        ),
        notification_type="PAYMENT",
        is_read=False,
    )

    db.add(notification)
    db.commit()
    db.refresh(payment)

except Exception:
    db.rollback()
    raise HTTPException(
        status_code=500,
        detail="Unable to process payment",
    )

return {
    "message": "Payment processed successfully",
    "payment_id": payment.id,
    "booking_id": payment.booking_id,
    "payment_method": payment.payment_method,
    "payment_status": payment.payment_status,
    "transaction_id": payment.transaction_id,
    "amount": payment.amount,
    "booking_status": booking.status,
}
