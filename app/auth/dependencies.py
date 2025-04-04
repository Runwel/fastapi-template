from fastapi import Depends
from app.core.security import role_required
from app.auth.models.user import User

def admin_or_dev_user(user: User = Depends(role_required(["ADMIN", "DEVELOPER"]))):
    """Reusable dependency for checking if the user is ADMIN or DEVELOPER."""
    return user