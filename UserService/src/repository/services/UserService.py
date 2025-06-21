
from UserService.src.repository.interfaces import UserRepositoryInterface
from UserService.src.repository.utils.UserPasswordManager import saltAndHashedPW
from UserService.src.schemas import UserSchema

class UserService:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository: UserRepositoryInterface = user_repository

    async def get_user(
        self,
        email:str,
    ) -> UserSchema.UserResponse:
        user: UserSchema.User = await self.user_repository.get_user(email)

        return UserSchema.UserResponse(
            email=user.email,
            is_active=user.is_active
        )
    
    async def create_user(
        self,
        email: str
    ) -> UserSchema.UserResponse:
        
        user = await self.user_repository.create_user(
            User_instance = UserSchema.User(
                email=email,
                is_active=True
            )
        )
        return UserSchema.UserResponse(
            email=user.email,
            is_active=user.is_active
        )

    async def reset_password(
        self,
        email: str,
        reset_password: UserSchema.ResetPassword
    ) -> UserSchema.UserResponse:

        hashed_pw = await saltAndHashedPW(reset_password.password)
        user = await self.user_repository.update_user(
            UserSchema.User(
                email=email,
                hashed_password=hashed_pw,
                is_active=True
            )
        )

        return UserSchema.UserResponse(
            email=user.email,
            is_active=user.is_active
        )

    async def deactivate_user(
        self,
        email: str
    ) -> UserSchema.UserResponse:

        user = await self.user_repository.update_user(
            UserSchema.User(
                email=email,
                is_active=False
            )
        )

        return UserSchema.UserResponse(
            email=user.email,
            is_active=user.is_active
        )
    
# The Repository Pattern in action. Here you can see how my UserService depends on the interface, which is an abstraction, instead of the actual implementation. 
# This means I can later make another implementation, e.g. DynamoDB, which implements the interface, and I would not need to change my service layer one bit. 
# This is one of the major reasons it is incredibly popular, and later you shall see even more benefits when we start writing unit tests.