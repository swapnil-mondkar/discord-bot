# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# loader.py

from commands import events, message

def setup_bot(bot):
    """
    Loads and sets up all required bot modules.

    This function is responsible for registering all events and commands 
    necessary for the bot to function properly.

    Args:
        bot (bot): The Discord bot bot instance to bind modules to.
    """
    # Register event handling module
    events.setup(bot)

    # Register message handling module
    message.setup(bot)

    # Log the successful loading of all modules
    print("All modules have been loaded successfully.")
