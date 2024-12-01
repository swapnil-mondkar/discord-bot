# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# purge.py

import discord
from bot.logger import log_to_mongo, log_error

def setup(bot):

    # Define the `/purge` command
    @bot.command()
    async def purge(ctx, limit: int, user: discord.User = None):
        # Delete the command message that triggered the purge
        await ctx.message.delete()

        # If a user is mentioned, delete their messages; otherwise, delete all messages
        if user:
            # Delete the last 'limit' messages from the specified user
            deleted = await ctx.channel.purge(limit=limit, check=lambda m: m.author == user)
            await ctx.send(f"Deleted {len(deleted)} messages from {user.name}.", delete_after=5)
        else:
            # Delete the last 'limit' messages from the entire channel
            deleted = await ctx.channel.purge(limit=limit)
            await ctx.send(f"Deleted {len(deleted)} messages from the channel.", delete_after=5)
