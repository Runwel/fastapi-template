# Auto-import all models when importing `app.models`
from app.auth.models.user import User
from app.auth.models.role import Role
from app.auth.models.file import File
from app.auth.models.audit_logs import AuditLog
# Add more models here as you create them
