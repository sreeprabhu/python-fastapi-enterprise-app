from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
import logging

from UserService.src.db.settings import DatabaseType, get_settings
from UserService.src.logging_config import setup_logging
from UserService.src.middleware.transaction_id_middleware import TransactionIdMiddleware

from .routes import UserController
from .exceptions import BaseAppException

setup_logging()
logger = logging.getLogger(__name__)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code (runs before application startup)
    logger.info("Running startup tasks...")

    # Initialize settings
    settings = get_settings()
    if settings.DATABASE_TYPE == DatabaseType.POSTGRES:
        # Create an async engine
        engine = create_async_engine(settings.POSTGRES_DATABASE_URL, echo=True, future=True)

        # Create an async sessionmaker factory - we can now request the app.state.postgres_session from other parts of our code to generate a new async Session to interact with our database.
        app.state.postgres_session = async_sessionmaker(
            bind=engine,
            expire_on_commit=False,  # optional: objects stay active after commit
            class_=AsyncSession
        )

    logger.info("Startup tasks completed")
    yield
    # Shutdown code (runs after application shutdown)
    logger.info("Running shutdown tasks...")
    logger.info("Shutdown tasks completed")
    # This is where you put code that was previously in @app.on_event("shutdown")

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "PUT"],
    allow_headers=["Authorization", "Content-Type"]
)

# Enable Transaction ID middleware
app.add_middleware(TransactionIdMiddleware)

# Global exception handler
@app.exception_handler(BaseAppException)
async def app_exception_handler(request, exc):
    logger.error("Application error: %s", exc.message)
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message}
    )

# Routers
app.include_router(UserController.router)

# We include our UserController in our FastAPI app to make the endpoints accessible.
# Additionally, I make some simple CORS middleware, which allows us to access our endpoints from localhost:8000, which means I will later be able to interact with my container from outside the container. 
# This is necessary if I want to test my endpoints from my local machine using Postman. 
# Finally, I set up lifespan to prepare for start up and shutdown tasks.