
# Validate date range
if date_from and date_to and date_from > date_to:
    raise HTTPException(
        status_code=400,
        detail="date_from cannot be later than date_to",
    )

# Validate price range
if (
    min_price is not None
    and max_price is not None
    and min_price > max_price
):
    raise HTTPException(
        status_code=400,
        detail="min_price cannot exceed max_price",
    )

# Search by event name
if q and q.strip():
    query = query.filter(
        Event.name.ilike(f"%{q.strip()}%")
    )

# Filter by category
if category and category.strip():
    query = query.filter(
        Event.category.ilike(f"%{category.strip()}%")
    )

# Filter by location
if location and location.strip():
    query = query.filter(
        Event.location.ilike(f"%{location.strip()}%")
    )

# Filter by date range
if date_from:
    query = query.filter(
        Event.event_date >= date_from
    )

if date_to:
    query = query.filter(
        Event.event_date <= date_to
    )

# Filter by price range
if min_price is not None:
    query = query.filter(
        Event.price >= min_price
    )

if max_price is not None:
    query = query.filter(
        Event.price <= max_price
    )

# Sort events
if sort_by == "price":
    query = query.order_by(
        Event.price.asc(),
        Event.id.asc(),
    )

elif sort_by == "popularity":
    query = (
        query.outerjoin(
            Review,
            Review.event_id == Event.id,
        )
        .group_by(Event.id)
        .order_by(
            func.count(Review.id).desc(),
            Event.id.asc(),
        )
    )

else:
    query = query.order_by(
        Event.event_date.asc(),
        Event.id.asc(),
    )
