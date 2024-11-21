# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# intents.py

import config
from discord import Intents
from discord.ext.commands import Bot

def setup_intents():
    # Create a default set of intents
    intents = Intents.default()

    # Enable intent to read message content (necessary for processing messages)
    intents.message_content = True

    # Enable intent to listen for member events (necessary for tracking when members join/leave)
    intents.members = True

    # Return the configured intents object
    return intents

def create_bot():
    """
    Create and configure the bot instance.
    
    Returns:
        Bot: The configured Discord Bot instance.
    """
    intents = setup_intents()
    bot = Bot(command_prefix = config.COMMAND_PREFIX, intents=intents)
    return bot