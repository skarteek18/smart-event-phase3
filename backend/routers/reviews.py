

if not event:
    raise HTTPException(
        status_code=404,
        detail="Event not found",
    )

# Reviews are allowed only after the event
now = datetime.now(timezone.utc)
event_date = event.event_date

if event_date.tzinfo is None:
    now = now.replace(tzinfo=None)

if event_date > now:
    raise HTTPException(
        status_code=400,
        detail="You can review this event after it has taken place",
    )

# Verify that the user has a confirmed booking
booking = (
    db.query(Booking)
    .filter(
        Booking.user_id == current_user.id,
        Booking.event_id == event.id,
        Booking.status == "CONFIRMED",
    )
    .first()
)

if not booking:
    raise HTTPException(
        status_code=403,
        detail="A confirmed booking is required to review this event",
    )

# Enforce one review per user per event
existing_review = (
    db.query(Review)
    .filter(
        Review.user_id == current_user.id,
        Review.event_id == event.id,
    )
    .first()
)

if existing_review:
    raise HTTPException(
        status_code=409,
        detail="You have already reviewed this event",
    )

review = Review(
    user_id=current_user.id,
    event_id=event.id,
    rating=payload.rating,
    review_text=payload.review_text,
)

try:
    db.add(review)
    db.commit()
    db.refresh(review)
except Exception:
    db.rollback()
    raise HTTPException(
        status_code=409,
        detail="Unable to save review. Check whether a review already exists.",
    )

return {
    "message": "Review submitted successfully",
    "id": review.id,
    "user_id": review.user_id,
    "event_id": review.event_id,
    "rating": review.rating,
    "review_text": review.review_text,
    "created_at": review.created_at,
}
