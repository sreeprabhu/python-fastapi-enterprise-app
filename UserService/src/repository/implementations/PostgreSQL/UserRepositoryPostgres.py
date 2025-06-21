
from UserService.src.repository.interfaces.UserRepositoryInterface import UserRepositoryInterface
from UserService.src.schemas import UserSchema

class UserRepository(UserRepositoryInterface):
    def __init__(self, db = None):
        self.db = db

    async def get_user(
        self, email:str
        ) -> UserSchema.User:
        
        return UserSchema.User(
            email=email,
            is_active=True
        )

    async def create_user(
        self,
        User_instance: UserSchema.User
    ) -> UserSchema.User:

        return UserSchema.User(
            email=User_instance.email,
            is_active=True if User_instance.is_active else False
        )
        

    async def update_user(
        self,
        User_instance: UserSchema.User
    ) -> UserSchema.User:
        
        return UserSchema.User(
            email=User_instance.email,
            is_active=User_instance.is_active
        )
    