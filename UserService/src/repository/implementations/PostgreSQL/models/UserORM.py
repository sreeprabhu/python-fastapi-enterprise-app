from tokenize import String

from sqlalchemy import Boolean, Column

class UserORM:
    __table__name = "users"
    __table__args = {"schema": "auth"}

    email = Column(String, primary_key=True, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
