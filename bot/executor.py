# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# executor.py

import bot.config as config
from commands.logger import log_error

def run_bot(bot):
    """
    Retrieves the bot token from the environment and starts the bot.

    This function checks for the bot's token in the environment variables 
    and starts the bot using that token. If the token is missing or there 
    is an error during startup, it logs an error and terminates the process.

    Args:
        bot (bot): The Discord bot bot instance to run.
    """
    # Retrieve the bot token from the config
    TOKEN = config.DISCORD_TOKEN

    # Check if the token is present
    if not TOKEN:
        error_message = "DISCORD_TOKEN not found in config file or environment variables."
        log_error(error_message)
        raise ValueError(error_message)

    try:
        # Start the bot using the provided token
        bot.run(TOKEN)

    except Exception as e:
        # Handle any errors that occur during bot startup
        error_message = f"Error starting the bot: {str(e)}"
        log_error(error_message)
        raise
