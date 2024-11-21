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

# MongoDB configuration
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "bot")

# Discord configuration
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_FOR_MESSAGE = os.getenv("CHANNEL_FOR_MESSAGE")
CHANNEL_FOR_LOGS = os.getenv("CHANNEL_FOR_LOGS")
