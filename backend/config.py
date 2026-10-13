

# Database configuration
DATABASE_URL: str = "sqlite:///./smartevent.db"

# JWT authentication settings
SECRET_KEY: str = "change-this-secret-before-deployment"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
JWT_ALGORITHM: str = "HS256"

# Frontend configuration
FRONTEND_URL: str = "http://localhost:5173"

# Payment configuration
PAYMENT_MODE: str = "simulation"

# Stripe test-mode configuration
STRIPE_SECRET_KEY: str = ""
STRIPE_WEBHOOK_SECRET: str = ""

# Environment configuration
ENVIRONMENT: str = "development"

model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    extra="ignore",
)
