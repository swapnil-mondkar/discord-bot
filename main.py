# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# main.py

"""
    Isko mat chhed, jab tak code ka pura gyaan na ho, samjha? - Swapnil
"""

from mybot.intents import create_bot
from mybot.loader import setup_bot
from mybot.executor import run_bot

# Create the bot instance
bot = create_bot()

# Setup external modules (events and commands)
setup_bot(bot)

# Run the bot with the token
run_bot(bot)
