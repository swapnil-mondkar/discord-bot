# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# bot.cogs.admin.command.py

from discord.ext import commands
from bot.extensions.logger import logger
from bot.utils.pagination import send_paginated_message

def setup(bot):

    db = bot.db
    cogs_collection = db["commands"]

    @bot.command()
    @commands.guild_only()
    async def commands(ctx):
        """Displays a list of available commands."""
        try:
            # Fetch all cogs from MongoDB
            cogs_list = list(cogs_collection.find())

            if not cogs_list:
                await ctx.send("No commands available right now.")
                return

            # Use the utility function to send a paginated message
            await send_paginated_message(
                ctx=ctx,
                items=cogs_list,
                title="Available Commands",
                description="Here's a list of all the commands you can use:"
            )
        except Exception as e:
            await ctx.send("⚠️ Something went wrong while fetching commands.")
            logger.log_error(f"Error fetching commands: {e}")
