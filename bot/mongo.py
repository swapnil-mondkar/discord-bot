# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# mongo.py

from pymongo import MongoClient
import bot.config as config

# MongoDB connection setup
def connect_mongo():
    # Get MongoDB URL and DB name from environment variables
    client = MongoClient(config.MONGO_URL)
    db = client[config.MONGO_DB]  # Use the database name from environment
    return db
