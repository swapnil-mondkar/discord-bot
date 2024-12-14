# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# bot.cogs.moderation.poll.py

import discord
from discord.ext import commands
from bot.extensions.logger import logger

def setup(bot):

    # Define the `/poll` command
    @bot.command()
    @commands.guild_only()
    async def poll(ctx, *, question: str):
        if not ctx.author.guild_permissions.manage_messages:
            await ctx.send("⚠️ You do not have permission to create polls.")
            return

        embed = discord.Embed(title="📊 Poll", description=question, color=discord.Color.blue())
        poll_message = await ctx.send(embed=embed)
        await poll_message.add_reaction("👍")  # Yes
        await poll_message.add_reaction("👎")  # No
