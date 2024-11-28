# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# intents.py

import config
import logging
from discord import Intents
from discord.ext.commands import Bot

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def setup_intents() -> Intents:
    """
    Set up and configure the Discord bot's intents.

    Returns:
        Intents: The configured Intents object.
    """
    # Create a default set of intents
    intents = Intents.default()

    # Enable specific intents
    intents.message_content = True  # Allow the bot to read message content
    intents.members = True  # Enable member tracking (join/leave events)

    # Log the enabled intents (you can expand this to log more details)
    logger.info("Intents configured: message_content, members")

    return intents

def create_bot() -> Bot:
    """
    Create and configure the Discord Bot instance.

    Returns:
        Bot: The configured Discord Bot instance.
    """
    intents = setup_intents()

    # Create the bot instance with the specified command prefix and intents
    bot = Bot(command_prefix=config.COMMAND_PREFIX, intents=intents)

    # Log successful bot creation
    logger.info(f"Bot created with command prefix: {config.COMMAND_PREFIX}")

    return bot
