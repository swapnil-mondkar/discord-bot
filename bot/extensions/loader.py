# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# bot/loader.py

"""
    This module dynamically loads and sets up all command modules in the `bot/cogs` directory,
    including nested folders (e.g., `bot/cogs/more`).
"""

import asyncio
import os
import importlib.util
import logging
from bot.extensions.logger import logger

def setup_bot(bot):
    """
    Automatically loads and sets up all command modules in the `bot/cogs` directory, 
    including nested folders.

    Args:
        bot (commands.Bot): The Discord bot instance to bind modules to.
    """
    # Define the root directory for command modules
    cogs_dir = os.path.join("bot", "cogs")

    # Check if the 'cogs' directory exists
    if not os.path.exists(cogs_dir):
        logger.log_to_file(logging.ERROR, f"Directory '{cogs_dir}' does not exist. No cogs to load.")
        return

    logger.log_to_file(logging.INFO, f"Loading command modules from '{cogs_dir}'...")

    # Walk through all subdirectories and files in the cogs directory
    for root, _, files in os.walk(cogs_dir):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                # Generate the module path (e.g., bot.cogs.more.example)
                relative_path = os.path.relpath(os.path.join(root, file), os.getcwd())
                module_name = relative_path.replace(os.sep, ".")[:-3]  # Replace '/' or '\' with '.' and remove '.py'

                try:
                    # Dynamically import the module
                    spec = importlib.util.find_spec(module_name)
                    if spec is None:
                        raise ModuleNotFoundError(f"Cannot find module: {module_name}")
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    # Call the `setup` function if it exists
                    if hasattr(module, "setup"):
                        # Check if setup is a coroutine
                        if asyncio.iscoroutinefunction(module.setup):
                            # Schedule the asynchronous setup function as a task
                            asyncio.run(module.setup(bot))
                        else:
                            # If setup is not asynchronous, call it directly
                            module.setup(bot)
                        logger.log_to_file(logging.INFO, f"Successfully loaded module: {module_name}")
                    else:
                        logger.log_to_file(logging.WARNING, f"Skipped module (no setup function): {module_name}")

                except ModuleNotFoundError as mnfe:
                    logger.log_to_file(logging.ERROR, f"Module not found: {module_name}. Error: {mnfe}")
                except Exception as e:
                    logger.log_to_file(logging.ERROR, f"Error loading module {module_name}: {e}")

    logger.log_to_file(logging.INFO, "All modules have been processed.")
