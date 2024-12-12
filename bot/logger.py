# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# bot/logger.py

"""
    A centralized logger module for handling file and MongoDB logging.
"""

import logging
from datetime import datetime
from bot.mongo import connect_mongo

class Logger:
    def __init__(self, log_file="bot.log", log_level=logging.ERROR):
        """
        Initialize the Logger instance for file and MongoDB logging.

        Args:
            log_file (str): The name of the log file (default: 'bot.log').
            log_level (int): Logging level (default: logging.ERROR).
        """
        # Setup file logging
        logging.basicConfig(
            filename=log_file,
            level=log_level,
            format="%(asctime)s [%(levelname)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        self.file_logger = logging.getLogger(__name__)

        # Setup MongoDB connection
        self.db = connect_mongo()
        self.logs_collection = self.db["logs"]

    def log_to_file(self, level, message):
        """
        Log a message to the file.

        Args:
            level (int): The logging level (e.g., logging.INFO, logging.ERROR).
            message (str): The message to log.
        """
        try:
            if level == logging.ERROR:
                self.file_logger.error(message)
            elif level == logging.WARNING:
                self.file_logger.warning(message)
            elif level == logging.INFO:
                self.file_logger.info(message)
            elif level == logging.DEBUG:
                self.file_logger.debug(message)
        except Exception as e:
            print(f"Failed to log to file: {e}")

    def log_to_mongo(self, author_name, author_id, message, channel_name):
        """
        Log an action or message to the MongoDB logs collection.

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
                "timestamp": datetime.utcnow(),
                "channel": channel_name,
                "message_length": len(message),
            }
            self.logs_collection.insert_one(log_entry)
            print(f"Logged message from {author_name} in channel {channel_name}.")
        except Exception as e:
            self.log_to_file(logging.ERROR, f"Failed to log to MongoDB: {e}")

    def log_error(self, error_message):
        """
        Log an error message to both the file and MongoDB.

        Args:
            error_message (str): The error message to log.
        """
        try:
            # Log to the file
            self.log_to_file(logging.ERROR, error_message)

            # Log to MongoDB
            self.logs_collection.insert_one({
                "error": error_message,
                "timestamp": datetime.utcnow(),
            })
        except Exception as e:
            print(f"Critical failure logging error: {e}")

# Initialize a global Logger instance
logger = Logger()