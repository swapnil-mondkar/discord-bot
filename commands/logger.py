# logger.py

from datetime import datetime
from mongo import connect_mongo

# Connect to MongoDB
db = connect_mongo()
logs_collection = db["logs"]  # Access the "logs" collection

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
