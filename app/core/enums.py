from enum import Enum

class RoleEnum(str, Enum):  # ✅ Inherits from str to return a string
    ADMIN = "ADMIN"
    DEVELOPER = "DEVELOPER"
    TEACHER = "TEACHER"
    STUDENT = "STUDENT"
    PARENT = "PARENT"
    REGISTRAR = "REGISTRAR"
    GUEST = "GUEST"

class PermissionEnum(str, Enum):
    CREATE = "CREATE"
    READ = "READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
