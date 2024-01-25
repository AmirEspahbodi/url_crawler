import logging
import os
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from app.core.config.app import AppConfig

# Create a logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Define the log file format
log_format = "%(asctime)s - %(levelname)s - %(message)s"

# Get the current date to use in the log file name
current_date = datetime.now().strftime("%Y-%m-%d")
log_filename = f"logs/{current_date}.log"

# Create the logger and set the log level
logger = logging.getLogger("fastapi")
logger.setLevel(logging.DEBUG)

# Create the file handler and set the log level
file_handler = TimedRotatingFileHandler(log_filename, when="midnight", backupCount=7)
file_handler.setLevel(logging.DEBUG)

# Set the log file format
formatter = logging.Formatter(log_format)
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

full_log = False


# Define the logging middleware
async def logging_middleware(request, call_next):
    if full_log:
        request_details = {
            "method": request.method,
            "url": str(request.url),
            "headers": dict(request.headers),
            "client_ip": request.client.host,
        }
        logger.info(f"Request: {request_details}")
    else:
        logger.info(
            f"Request: {request.method} {request.url} Client: {request.client.host}"
        )
    response = await call_next(request)
    return response
