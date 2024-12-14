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

from bot.extensions.intents import create_bot
from bot.extensions.loader import setup_bot
from bot.extensions.executor import run_bot

def main():
    """
    Main function to initialize and run the bot.

    Steps:
    1. Create the bot instance.
    2. Set up external modules (events and commands).
    3. Run the bot with the token.
    """
    try:
        # Step 1: Create the bot instance
        bot = create_bot()

        # Step 2: Setup events and command handlers
        setup_bot(bot)

        # Step 3: Run the bot
        run_bot(bot)

    except Exception as e:
        # Handle unexpected errors gracefully
        print(f"An error occurred while running the bot: {e}")

# Entry point for the script
if __name__ == "__main__":
    main()
