from abc import ABC, abstractmethod

from UserService.src.schemas import UserSchema

class UserRepositoryInterface(ABC):

    @abstractmethod
    async def get_user(self, email:str) -> UserSchema.User:
        pass
    
    @abstractmethod
    async def create_user(self, User_instance: UserSchema.User):
        pass

    @abstractmethod
    async def update_user(self, User_instance: UserSchema.User):
        pass

    #To achieve loose coupling between the service layer and the actual database implementation, I create an interface. This means my actual implementation implements this interface, and it also means my service layer does not depend on the actual implementation, but on the interface. You can also see here that we have defined that the get_user method must return a User which we defined in our UserSchemas.pyabove.