# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# bot/loader.py

"""
    This module dynamically loads and sets up all command modules in the `cogs` directory.
"""

import os
import importlib
import logging
from bot.logger import logger  # Import the global logger instance

def setup_bot(bot):
    """
    Automatically loads and sets up all command modules in the `cogs` directory.

    Args:
        bot (commands.Bot): The Discord bot instance to bind modules to.
    """
    # Define the directory containing command modules
    cogs_dir = "cogs"

    # Check if the 'cogs' directory exists
    if not os.path.exists(cogs_dir):
        logger.log_to_file(logging.ERROR, f"Directory '{cogs_dir}' does not exist. No cogs to load.")
        return

    logger.log_to_file(logging.INFO, f"Loading command modules from '{cogs_dir}'...")

    # Iterate through all Python files in the `cogs` directory
    for filename in os.listdir(cogs_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"{cogs_dir}.{filename[:-3]}"

            try:
                # Dynamically import the module
                module = importlib.import_module(module_name)

                # Call the `setup` function if it exists
                if hasattr(module, "setup"):
                    module.setup(bot)
                    logger.log_to_file(logging.INFO, f"Successfully loaded module: {module_name}")
                else:
                    logger.log_to_file(logging.WARNING, f"Skipped module (no setup function): {module_name}")

            except ModuleNotFoundError as mnfe:
                logger.log_to_file(logging.ERROR, f"Module not found: {module_name}. Error: {mnfe}")
            except Exception as e:
                logger.log_to_file(logging.ERROR, f"Error loading module {module_name}: {e}")

    logger.log_to_file(logging.INFO, "All modules have been processed.")
