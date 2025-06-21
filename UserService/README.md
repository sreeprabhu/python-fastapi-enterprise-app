# How is a request handled?

### In the previous section I presented my initial codebase for my FastAPI User Service. I will now go through, step by step, when my endpoint receives a request. I will use GET /users?email=test@example.comas my example:

#### 1. End-user makes a GET /users?email=test@example.com request.

#### 2. UserController sets user_service as a new UserService instance by calling the get_user_service function which is injected into the endpoint. In this example the user_service.repository is the PostgreSQL implementation of the interface_UserRepository.

#### 3. user_service.get_user(email=’test@example.com’) is awaited.

#### 4. The user_service.get_user method awaits user_service.repository.get_user(email=’test@example.com’) and since our repository is the PostgreSQL implementation, that is the specific method that is called. This method in the PostgreSQL implementation simply returns a User, as defined in UserSchemas.py, with email set as the one used in the request, in this case test@example.com.

#### 5. user_service_get_user then transforms the Userinto a UserResponse, which is then returned to the UserController.

#### 6. The UserController returns the UserResponse to the end-user.
