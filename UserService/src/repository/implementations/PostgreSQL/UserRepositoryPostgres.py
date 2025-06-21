
from UserService.src.exceptions import BaseAppException, ResourceNotFoundException
from UserService.src.repository.interfaces.UserRepositoryInterface import UserRepositoryInterface
from UserService.src.schemas import UserSchema
import logging

logger = logging.getLogger(__name__)

class UserRepository(UserRepositoryInterface):
    def __init__(self, db = None):
        self.db = db

    async def get_user(
        self, email:str
        ) -> UserSchema.User:

        # Dummy logging - log method was called
        logger.info("PostgreSQL: get_user method called")
        
        try:
            # Dummy exception
            if email == "nonexistent@example.com":
                logger.warning(f"User with email {email} not found")
                raise ResourceNotFoundException(f"User with email {email} not found")
            
            return UserSchema.User(
                email=email,
                is_active=True
            )
        
        # Catch the ResourceNotFoundException and raise to other layers
        except ResourceNotFoundException:
            raise

        # Catch the Uncaught exception and raise to other layers as BaseAppException
        except Exception as e:
            logger.exception(f"Error getting user: {str(e)}")
            raise BaseAppException(f"Internal database error: {str(e)}") from e

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
    