# smart-event-phase3

SmartEvent – Phase 3

Event Discovery & Ticket Booking Platform

SmartEvent is a full-stack event discovery and ticket booking application developed using FastAPI, Python, React (Vite), SQLAlchemy, and SQL. Phase 3 extends the existing platform with payment processing, coupon and discount management, event reviews, notifications, advanced search, and professional UI/UX enhancements.

Technologies Used

Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- JWT Authentication
- SQLite / PostgreSQL

Frontend

- React.js
- Vite
- Tailwind CSS
- Axios
- React Router
- Lucide React

Modules Implemented

Module 12: Event Payment System

- Payment checkout functionality.
- Payment records linked to bookings.
- Payment status tracking: "PENDING", "SUCCESS", and "FAILED".
- Unique transaction reference storage.
- Booking status updates after successful payment.
- Payment confirmation page displaying transaction details.
- Support for payment simulation and extensibility for Stripe test mode.

Module 13: Coupon & Discount System

- Coupon validation before application.
- Percentage-based and fixed-amount discounts.
- Minimum booking amount validation.
- Coupon expiry validation.
- Usage limit and activation checks.
- Discount breakdown and final payable amount.

Module 14: Event Feedback & Ratings

- Submit event reviews and ratings.
- Star rating system from 1 to 5.
- Retrieve reviews for individual events.
- Calculate average event ratings.
- Edit and delete personal reviews.
- Restrict reviews to eligible users with confirmed bookings.

Module 15: Advanced Notification System

- Booking and payment notifications.
- Notification history.
- Notification categories: "EVENT", "BOOKING", "PAYMENT", and "SYSTEM".
- Mark individual notifications as read.
- Mark all notifications as read.
- Extensible notification triggers for event updates and reminders.

Module 16: Event Search & Filtering

- Search events by name.
- Filter by category and location.
- Filter by date range.
- Sort events by date, price, and popularity.
- Paginated API results.
- Responsive event discovery interface.

Module 17: Professional UI/UX Enhancement

- Modern event cards with hover effects.
- Responsive layouts for mobile and desktop.
- Improved typography, spacing, and navigation.
- Event search and filter interface.
- Booking checkout and payment confirmation pages.
- Review submission and notification history pages.
- Loading indicators and user feedback messages.

Project Structure

SmartEvent/
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   ├── config.py
│   ├── requirements.txt
│   └── routers/
│       ├── payments.py
│       ├── coupons.py
│       ├── reviews.py
│       ├── notifications.py
│       └── events.py
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── App.jsx
│       ├── api.js
│       ├── index.css
│       ├── main.jsx
│       ├── components/
│       └── pages/
├── .gitignore
└── README.md

Installation and Setup

1. Clone the Repository

git clone YOUR_GITHUB_REPOSITORY_URL
cd SmartEvent

2. Set Up the Backend

cd backend
python -m venv .venv

Activate the virtual environment.

Windows:

.venv\Scripts\activate

Linux / macOS:

source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Configure the environment variables in a ".env" file using ".env.example" as a template.

Start the FastAPI server:

uvicorn main:app --reload

Backend URL: "http://localhost:8000"

API documentation: "http://localhost:8000/docs"

3. Set Up the Frontend

Open a new terminal:

cd frontend
npm install
npm run dev

Frontend URL: "http://localhost:5173"

Important API Endpoints

Method| Endpoint| Description
POST| "/auth/register"| Register a user
POST| "/auth/login"| Authenticate a user
GET| "/events"| Search and filter events
GET| "/events/{event_id}"| Retrieve event details
POST| "/coupons/validate"| Validate a coupon
POST| "/payments/checkout"| Process a simulated payment
GET| "/payments/{payment_id}"| Retrieve payment details
POST| "/reviews"| Submit an event review
GET| "/reviews/event/{event_id}"| Retrieve event reviews
PUT| "/reviews/{review_id}"| Update a personal review
DELETE| "/reviews/{review_id}"| Delete a personal review
GET| "/notifications"| Retrieve notifications
PATCH| "/notifications/{id}/read"| Mark a notification as read
PATCH| "/notifications/read-all"| Mark all notifications as read

Security Features

- JWT authentication for protected APIs.
- Password hashing.
- Pydantic request validation.
- Review ownership verification.
- Booking ownership checks during payment.
- Coupon expiry and usage limit validation.
- Environment-based configuration.

Testing

Use FastAPI Swagger UI to test the backend endpoints:

1. Register a user.
2. Log in and obtain a JWT access token.
3. Authorize protected endpoints.
4. Create an event and booking using the existing booking module.
5. Test payment processing and confirmation.
6. Test coupon validation.
7. Submit and retrieve event reviews.
8. Verify notification and event filtering functionality.

Future Enhancements

- Integrate Stripe Checkout and verified payment webhooks.
- Add automated backend tests using Pytest.
- Add Alembic database migrations.
- Implement scheduled event reminders and email notifications.
- Add booking analytics and organizer dashboards.
- Improve payment idempotency and transaction handling.
- Deploy the application using production-ready infrastructure.

Important Note

The included payment simulation is intended for development and demonstration only. Production deployment requires a real payment gateway with server-side verification. Coupon application, notification triggers, and database relationships must be integrated with the existing project modules before these features can be considered production-ready.

Conclusion

SmartEvent Phase 3 extends the event booking platform with payment workflows, promotional discounts, event ratings, notifications, enhanced discovery, and a responsive user interface. These modules provide a foundation for a more complete and user-friendly event management platform.

---

Project: SmartEvent – Event Discovery & Ticket Booking System
Phase: Phase 3 – Advanced Features and UI/UX Enhancement
Backend: FastAPI
Frontend: React (Vite)
Database: SQLite / PostgreSQL
