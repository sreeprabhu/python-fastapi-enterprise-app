

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from UserService.src.db.db_context import db_context
from UserService.src.db.factory import create_user_repository
from UserService.src.repository.implementations.PostgreSQL.UserRepositoryPostgres import UserRepository
from UserService.src.repository.interfaces.UserRepositoryInterface import UserRepositoryInterface
from UserService.src.repository.services.UserService import UserService

async def get_user_repository(db: AsyncSession = Depends(db_context)) -> UserRepositoryInterface:
    """
    Creates the appropriate repository based on configuration.
    The db parameter will be a database session for PostgreSQL or None for DynamoDB.
    """

    return create_user_repository(db)

async def get_user_service(user_repository: UserRepositoryInterface = Depends(get_user_repository)) -> UserService:
    return UserService(user_repository)

# Implementation - 1

# Now it becomes clear what we are injecting into our endpoints. 
# Right now we are not injecting real database sessions, but later in this series you will see how we extend this to actual database implementations with real PostgreSQL and DynamoDB async sessions.
# It also becomes clear that we achieve loose coupling wrt. our database when we inject an abstract repository interface (rather than a concrete implementation) into our service and controller layers.
# This means our business logic depends only on the interface, making it easy to swap out or extend database backends-such as replacing a PostgreSQL implementation with a DynamoDB implementation without changing the rest of our application code.
# For now, we are injecting our PostgresUserRepository, which obviously defeats the point. Later, when we actually implement our PostgreSQL and DynamoDB database backends, we will implement a similar dependency for get_user_repository as get_user_service and then actually achieve loose coupling.

# Implementation - 2

# These are the actual dependencies we are injecting into our endpoint — you might recall these from part 3. 
# The difference now is that we have sorted our tight coupling from part 3, as our get_user_repository now depends on db_context. 
# This means we can now change db_context to return another Session. 
# Later we will implement DynamoDB and it will become clear that our endpoints will not be tightly coupled to the database we have chosen.