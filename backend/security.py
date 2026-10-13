

from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from config import settings
from database import get_db
from models import User

==============================

JWT Configuration

==============================

ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(
tokenUrl="/auth/login"
)

==============================

Password Hashing

==============================

pwd_context = CryptContext(
schemes=["bcrypt"],
deprecated="auto",
)

def hash_password(password: str) -> str:
"""Hash a password before storing it."""
return pwd_context.hash(password)

def verify_password(
plain_password: str,
hashed_password: str,
) -> bool:
"""Verify a password against its stored hash."""
return pwd_context.verify(
plain_password,
hashed_password,
)

==============================

JWT Token Generation

==============================

def create_access_token(user_id: int) -> str:
"""Create a signed JWT access token."""
expires_at = datetime.now(timezone.utc) + timedelta(
minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
)

payload = {
    "sub": str(user_id),
    "exp": expires_at,
    "iat": datetime.now(timezone.utc),
}

return jwt.encode(
    payload,
    settings.SECRET_KEY,
    algorithm=ALGORITHM,
)

==============================

Current Authenticated User

==============================

def get_current_user(
token: str = Depends(oauth2_scheme),
db: Session = Depends(get_db),
) -> User:
"""Validate a JWT and return its active user."""

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid or expired authentication token",
    headers={"WWW-Authenticate": "Bearer"},
)

try:
    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[ALGORITHM],
    )

    subject = payload.get("sub")

    if not subject:
        raise credentials_exception

    user_id = int(subject)

except (JWTError, ValueError, TypeError):
    raise credentials_exception

user = (
    db.query(User)
    .filter(
        User.id == user_id,
        User.is_active.is_(True),
    )
    .first()
)

if user is None:
    raise credentials_exception

return user

==============================

Role-Based Authorization

==============================

def require_roles(*allowed_roles: str):
"""Restrict an endpoint to specified user roles."""

def role_checker(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )

    return current_user

return role_checker

==============================

Example Usage

==============================

Protect an endpoint:

@app.get("/profile")

def get_profile(

current_user: User = Depends(get_current_user)

):

return {

"id": current_user.id,

"email": current_user.email,

"role": current_user.role,

}

Admin-only endpoint:

@app.get("/admin/dashboard")

def admin_dashboard(

current_user: User = Depends(require_roles("admin"))

):

return {"message": "Welcome, admin"}
