class BaseAppException(Exception):
    """Base exception for our application"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class ResourceNotFoundException(BaseAppException):
    """Raised when a requested resource is not found"""
    def __init__(self, message: str):
        super().__init__(message, status_code=404)


# This is how we define our custom exceptions in our FastAPI application. 
# It basically returns the message from the exception alongside an http status code. 
# Additionally the exceptions inherits from the custom BaseAppException. 
# The purpose is that every uncaught exception is returned to the end-user as a BaseAppException with http status code 500, which means Internal Server Error. 
# Ideally, we will never return these, but as previously stated we can use our logs to track when these occur, and implement new custom exceptions to handle them reasonably. 
# Sometimes we will want to return an Internal Server Error, but we don’t want it to then be the unhandled BaseAppException but rather something like a custom ConnectionException, which inherits from BaseAppException, if e.g. our service is unable connect to our database.