# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# loader.py

import os
import importlib
import logging

def setup_bot(bot):
    """
    Automatically loads and sets up all command modules in the `commands` directory.

    Args:
        bot (cogs.Bot): The Discord bot instance to bind modules to.
    """
    # Define the directory containing command modules
    cogs_dir = "cogs"

    # Initialize logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Iterate through all Python files in the `cogs` directory
    for filename in os.listdir(cogs_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"cogs.{filename[:-3]}"

            try:
                # Dynamically import the module
                module = importlib.import_module(module_name)

                # Call the `setup` function if it exists
                if hasattr(module, "setup"):
                    module.setup(bot)
                    logger.info(f"Loaded module: {module_name}")
                else:
                    logger.warning(f"Skipped module (no setup function): {module_name}")
            
            except Exception as e:
                logger.error(f"Error loading module {module_name}: {e}")

    logger.info("All modules have been loaded successfully.")
