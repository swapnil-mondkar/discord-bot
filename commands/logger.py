# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# logger.py

import logging
from datetime import datetime
from mybot.mongo import connect_mongo

# Connect to MongoDB
db = connect_mongo()
logs_collection = db["logs"]  # Access the "logs" collection

# File Logger Setup
logging.basicConfig(
    filename = "bot.log",  # Log file name
    level = logging.ERROR,  # Log errors and above
    format = "%(asctime)s [%(levelname)s]: %(message)s",  # Log format
    datefmt = "%Y-%m-%d %H:%M:%S",  # Date format
)

def log_to_mongo(author_name: str, author_id: str, message: str, channel_name: str):
    """
    Logs an action or message to the MongoDB logs collection.

    Args:
        author_name (str): The name of the message author.
        author_id (str): The ID of the message author.
        message (str): The message content.
        channel_name (str): The name of the channel where the message was sent.
    """
    try:
        log_entry = {
            "author": author_name,
            "author_id": author_id,
            "message": message,
            "timestamp": datetime.utcnow(),  # Use UTC for consistent timestamping
            "channel": channel_name,  # Add channel name for better context
            "message_length": len(message)  # Log the message length
        }

        logs_collection.insert_one(log_entry)
        print(f"Logged message from {author_name} in channel {channel_name}.")
    except Exception as e:
        print(f"Failed to log to MongoDB: {e}")

def log_error(error_message: str):
    """
    Logs an error message to both the .log file and MongoDB.

    Args:
        error_message (str): The error message to log.
    """
    try:
        # Log to .log file
        logging.error(error_message)

    except Exception as e:
        print(f"Critical logging failure: {e}")