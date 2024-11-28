# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# config.py

import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

def get_env_variable(var_name, default=None, required=False):
    """
    Fetches an environment variable and raises an error if it's missing and required.

    Args:
        var_name (str): The name of the environment variable to fetch.
        default (str, optional): Default value to return if the variable is not found. Defaults to None.
        required (bool, optional): If True, an error will be raised if the variable is not found. Defaults to False.

    Returns:
        str: The value of the environment variable.
    """
    value = os.getenv(var_name, default)
    if required and value is None:
        raise ValueError(f"Environment variable {var_name} is required but not set.")
    return value

# MongoDB Configuration
MONGO_URL = get_env_variable("MONGO_URL", "mongodb://localhost:27017")
MONGO_DB = get_env_variable("MONGO_DB", "bot")

# Discord Bot Configuration
DISCORD_TOKEN = get_env_variable("DISCORD_TOKEN", required=True)
CHANNEL_FOR_MESSAGE = get_env_variable("CHANNEL_FOR_MESSAGE", required=True)
CHANNEL_FOR_LOGS = get_env_variable("CHANNEL_FOR_LOGS", required=True)

# Command Configuration
COMMAND_PREFIX = get_env_variable("COMMAND_PREFIX", "!")
