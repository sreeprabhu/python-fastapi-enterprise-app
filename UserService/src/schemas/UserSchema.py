from typing import Optional
from pydantic import BaseModel, model_validator
from typing_extensions import Self

class User(BaseModel):
    email: str
    hashed_password: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(BaseModel):
    email: str
    is_active: bool

class ResetPassword(BaseModel):
    password: str
    password_repeat: str

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.password != self.password_repeat:
            raise ValueError('Passwords do not match')
        return self
    
# Pydantic is a popular data validation library, and it is widely used for FastAPI applications. 
# It works very well in FastAPI applications, because request bodies are automatically validated when using Pydantic, e.g. are the required fields present with the correct data types in the request body. 
# In the above you can also see a custom model_validator which checks whether the two passwords, password and password_repeat, are equal. 
# This is relevant when a user sends a request to change their password, as they will only be able to do so, if the two passwords they provide are equal. 
# You will see extensive use of these User schemas throughout the application.