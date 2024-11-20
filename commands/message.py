# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# message.py

from discord import Message
from datetime import datetime
from mongo import connect_mongo  # Import the MongoDB connection function

# Connect to MongoDB
db = connect_mongo()
logs_collection = db["logs"]  # Access the "logs" collection

def setup(client):
    @client.event
    async def on_message(message: Message):
        if message.author == client.user:
            return

        try:
            # Prepare log entry
            log_entry = {
                "author": message.author.name,
                "author_id": str(message.author.id),
                "message": message.content,
                "timestamp": datetime.utcnow(),  # Use UTC for consistent timestamping
                "channel": message.channel.name,  # Add channel name for better context
                "message_length": len(message.content)  # Log the message length
            }

            # Insert the log entry into the "logs" collection
            logs_collection.insert_one(log_entry)
        except Exception as e:
            print(f"Error in Storing Logs.")
        
        print(f"Bot User: {client.user}")
        print(f"Message from {message.author}: {message.content}")

        # Process user message
        user_message = message.content
        await send_message(message, user_message)

# Utility function to send messages
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print("Empty message received.")
        return

    response = f"Hello! You said: {user_message}"
    await message.channel.send(response)
