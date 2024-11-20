# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# executor.py

import os

def run_bot(client):
    """
    Retrieves the bot token from the environment and starts the bot.
    
    This function checks for the bot's token in the environment variables 
    and starts the bot using that token. If the token is missing or there 
    is an error during startup, it will print an error message.

    Args:
        client (Client): The Discord bot client instance to run.
    """
    # Retrieve the bot token from the environment
    TOKEN = os.getenv('DISCORD_TOKEN')

    # If the token is not found, print an error and exit
    if not TOKEN:
        print("DISCORD_TOKEN not found in .env file.")
        exit()

    try:
        # Start the bot using the provided token
        client.run(TOKEN)
    except Exception as e:
        # Handle any errors that occur during bot startup
        print(f"Error starting the bot: {e}")
