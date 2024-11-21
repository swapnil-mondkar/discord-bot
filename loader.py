# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# loader.py

import os
import importlib

def setup_bot(bot):
    """
    Automatically loads and sets up all command modules in the `commands` directory.

    This function dynamically imports and registers all modules from the `commands` 
    directory, ensuring all events and commands are properly initialized.

    Args:
        bot (commands.Bot): The Discord bot instance to bind modules to.
    """
    # Define the directory containing command modules
    commands_dir = "commands"

    # Iterate through all Python files in the `commands` directory
    for filename in os.listdir(commands_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            # Extract the module name (without .py)
            module_name = f"{commands_dir}.{filename[:-3]}"

            try:
                # Import the module dynamically
                module = importlib.import_module(module_name)

                # Call the `setup` function in the module, passing the bot
                if hasattr(module, "setup"):
                    module.setup(bot)
                    print(f"Loaded module: {module_name}")
                else:
                    print(f"Skipped module (no setup function): {module_name}")

            except Exception as e:
                print(f"Error loading module {module_name}: {e}")

    # Log the successful loading of all modules
    print("All modules have been loaded successfully.")
