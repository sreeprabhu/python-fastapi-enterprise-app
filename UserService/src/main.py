from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from .routes import UserController

import logging
logger = logging.getLogger(__name__)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code (runs before application startup)
    logger.info("Running startup tasks...")
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

app.include_router(UserController.router)

# We include our UserController in our FastAPI app to make the endpoints accessible.
# Additionally, I make some simple CORS middleware, which allows us to access our endpoints from localhost:8000, which means I will later be able to interact with my container from outside the container. 
# This is necessary if I want to test my endpoints from my local machine using Postman. 
# Finally, I set up lifespan to prepare for start up and shutdown tasks.