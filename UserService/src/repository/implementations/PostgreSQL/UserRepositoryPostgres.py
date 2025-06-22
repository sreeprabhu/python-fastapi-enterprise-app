from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from UserService.src.exceptions import BaseAppException, ResourceNotFoundException
from UserService.src.repository.implementations.PostgreSQL.models import UserORM
from UserService.src.repository.interfaces.UserRepositoryInterface import UserRepositoryInterface
from UserService.src.schemas import UserSchema

logger = logging.getLogger(__name__)

class UserRepository(UserRepositoryInterface):
    def __init__(self, db = AsyncSession):
        self.db = db

    async def get_user(
        self, email:str
        ) -> UserSchema.User:

        # Dummy logging - log method was called
        logger.info("PostgreSQL: get_user method called")
        
        try:
            stmt = select(UserORM).where(UserORM.email == email)
            result = await self.db.execute(stmt)
            db_user = result.scalar_one_or_none()

            if db_user:    
                return UserSchema.User(
                    email=db_user.email,
                    is_active=db_user.is_active
                )
            else:
                logger.warning(f"User with email {email} not found")
                raise ResourceNotFoundException(f"User with email {email} not found")

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
    