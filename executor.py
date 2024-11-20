# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# executor.py

import config
from commands.logger import log_error

def run_bot(bot):
    """
    Retrieves the bot token from the environment and starts the bot.
    
    This function checks for the bot's token in the environment variables 
    and starts the bot using that token. If the token is missing or there 
    is an error during startup, it will print an error message.

    Args:
        bot (bot): The Discord bot bot instance to run.
    """
    # Retrieve the bot token from the environment
    TOKEN = config.DISCORD_TOKEN

    # If the token is not found, print an error and exit
    if not TOKEN:
        log_error("DISCORD_TOKEN not found in .env file.")
        exit()

    try:
        # Start the bot using the provided token
        bot.run(TOKEN)
    except Exception as e:
        # Handle any errors that occur during bot startup
        log_error(f"Error starting the bot: {e}")
