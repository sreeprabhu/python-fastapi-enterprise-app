# Run App - local

### go to root folder, then run:

- uvicorn UserService.src.main:app --reload

# Run App - docker

### run docker compose in watch mode:

- docker compose up --watch

### if you do any lcoal changes, do following

- docker compose down -v
- docker compose build --no-cache
- docker compose up --watch

# How is a request handled?

### In the previous section I presented my initial codebase for my FastAPI User Service. I will now go through, step by step, when my endpoint receives a request. I will use GET /users?email=test@example.comas my example:

- End-user makes a GET /users?email=test@example.com request.

- UserController sets user_service as a new UserService instance by calling the get_user_service function which is injected into the endpoint. In this example the user_service.repository is the PostgreSQL implementation of the interface_UserRepository.

- user_service.get_user(email=’test@example.com’) is awaited.

- The user_service.get_user method awaits user_service.repository.get_user(email=’test@example.com’) and since our repository is the PostgreSQL implementation, that is the specific method that is called. This method in the PostgreSQL implementation simply returns a User, as defined in UserSchemas.py, with email set as the one used in the request, in this case test@example.com.

- user_service_get_user then transforms the Userinto a UserResponse, which is then returned to the UserController.

- The UserController returns the UserResponse to the end-user.

# Part - 4

## ORM (Object-relational Mapper)

- First we need to understand the role of an ORM. The purpose of an ORM is to make a bridge between object-oriented code, in our case Python, and relational databases, in our case PostgreSQL. Instead of writing raw SQL, we can leverage ORM tools to interact with our relational database using familiar programming constructs. You define models as classes, and the ORM handles translating these objects to database tables and vice versa.

- SQLAlchemy is probably the most widely used ORM library in Python, and the simplicity of using it makes it clear why. We simply make our ORM model, which matches our table definition from before, and state the name of the table and table schema, and we are pretty much good to go. We are now able to interact with our relational database, PostgreSQL, in a pythonic manner using this ORM object.

## Engine, Session and Session Factory

### Engine

- The Engine is created once on start-up of our application, and manages the connection pool to our PostgreSQL database. This is only created once on start-up.

### Session

- The database Session is created on a per-request basis and is used to interact with our PostgreSQL database. Sessions are closed when the request is finished.

### Session Factory

- A Session Factory generates sessions. Specifically we will create a Session Factory to create a Session per request, as described above.

- In our application we will use an asynchronous engine and asynchronous sessions. We use asynchronous programming throughout the FastAPI application as we want requests to be non-blocking

- This is well-known best practise in FastAPI applications. When we use async behaviour in our engine and session, we simply ensure that database operations are also non-blocking.

# Part - 5

- In this section, we’ve demonstrated how to inject a database using dependency injection and achieve loose coupling between our endpoints and our database of choice.
- To summarise, we will quickly go through, step by step, what happens when an end-user sends a request:

1. end-user sends GET /users?email=test@example.com
2. Our dependency injection Depends(get_user_service) is called and assigned to variable user_service .
3. get_user_service depends on get_user_repository, which depends on db_context.
   From db_contextwe call our BaseSettingsto figure out, which dependency function to return. The settings are set to PostgreSQL, and thus db = Depends(db_context) sets dbto an async PostgreSQL Session.
4. get_user_repository now returns an instance of UserRepository, where the db of that instance is set to the async PostgreSQL Session.
5. get_user_service now returns an instance of UserService, where the repository is the UserRepository returned from get_user_repository before.
6. user_service is finally set to an instance of UserService, where its user_repositoryis an actual PostgreSQL implementation, with an actual async PostgreSQL Session to use for interacting with the database.
