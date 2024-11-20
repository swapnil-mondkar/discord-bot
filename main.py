# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# main.py

from dotenv import load_dotenv
from discord import Client
from intents import setup_intents
from loader import setup_bot
from executor import run_bot
from mongo import connect_mongo

# Create the client with intents
client = Client(intents=setup_intents())

# Setup external modules (events and message)
setup_bot(client)

# Run the bot with the token
run_bot(client)

# Connect to the local MongoDB database
db = connect_mongo()
