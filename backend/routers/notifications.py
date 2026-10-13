

if unread_only:
    query = query.filter(Notification.is_read.is_(False))

total = query.count()

notifications = (
    query.order_by(Notification.created_at.desc())
    .offset(skip)
    .limit(limit)
    .all()
)

unread_count = (
    db.query(Notification)
    .filter(
        Notification.user_id == current_user.id,
        Notification.is_read.is_(False),
    )
    .count()
)

return {
    "total": total,
    "unread_count": unread_count,
    "notifications": [
        {
            "id": notification.id,
            "title": notification.title,
            "message": notification.message,
            "notification_type": notification.notification_type,
            "is_read": notification.is_read,
            "created_at": notification.created_at,
        }
        for notification in notifications
    ],
}
