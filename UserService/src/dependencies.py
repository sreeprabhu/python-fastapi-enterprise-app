

from fastapi import Depends
from UserService.src.repository.implementations.PostgreSQL.UserRepositoryPostgres import UserRepository
from UserService.src.repository.interfaces import UserRepositoryInterface
from UserService.src.repository.services import UserService

async def get_user_repository() -> UserRepositoryInterface:
    return UserRepository()

async def get_user_service(user_repository: UserRepositoryInterface = Depends(get_user_repository)):
    return UserService(user_repository)

# Now it becomes clear what we are injecting into our endpoints. 
# Right now we are not injecting real database sessions, but later in this series you will see how we extend this to actual database implementations with real PostgreSQL and DynamoDB async sessions.
# It also becomes clear that we achieve loose coupling wrt. our database when we inject an abstract repository interface (rather than a concrete implementation) into our service and controller layers.
# This means our business logic depends only on the interface, making it easy to swap out or extend database backends-such as replacing a PostgreSQL implementation with a DynamoDB implementation without changing the rest of our application code.
# For now, we are injecting our PostgresUserRepository, which obviously defeats the point. Later, when we actually implement our PostgreSQL and DynamoDB database backends, we will implement a similar dependency for get_user_repository as get_user_service and then actually achieve loose coupling.