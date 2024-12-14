# Copyright (c) 2024 NULL Lab
# All rights reserved.
#
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# bot/intents.py

"""
    This module initializes and configures the Discord bot's intents and instance.
"""

import logging
from discord import Intents
from discord.ext.commands import Bot
from bot.extensions.config import COMMAND_PREFIX
from bot.extensions.mongo import connect_mongo
from bot.extensions.logger import logger

def setup_intents() -> Intents:
    """
    Set up and configure the Discord bot's intents.

    Returns:
        Intents: The configured Intents object.
    """
    try:
        # Create a default set of intents
        intents = Intents.default()

        # Enable specific intents
        intents.message_content = True  # Allow the bot to read message content
        intents.members = True  # Enable member tracking (join/leave events)

        # Log the enabled intents
        logger.log_to_file(logging.INFO, "Intents configured: message_content=True, members=True")

        return intents
    except Exception as e:
        logger.log_to_file(logging.ERROR, f"Error setting up intents: {e}")
        raise

def create_bot() -> Bot:
    """
    Create and configure the Discord Bot instance.

    Returns:
        Bot: The configured Discord Bot instance.
    """
    try:
        # Setup Discord intents
        intents = setup_intents()

        # Create the bot instance
        bot = Bot(command_prefix=COMMAND_PREFIX, intents=intents)

        # Establish database connection
        bot.db = connect_mongo()
        logger.log_to_file(logging.INFO, "Database connection established for the bot.")
        # Log successful bot creation
        logger.log_to_file(logging.INFO, f"Bot created with command prefix: '{COMMAND_PREFIX}'")

        return bot
    except Exception as e:
        logger.log_to_file(logging.ERROR, f"Error creating the bot: {e}")
        raise
