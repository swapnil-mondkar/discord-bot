# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# bot.cogs.moderation.announce.py

import discord
from discord.ext import commands
from bot.extensions.logger import logger

def setup(bot):

    # Define the `/announce` command
    @bot.command()
    @commands.guild_only()
    async def announce(ctx, channel: discord.TextChannel = None, *, message: str = None):
        if not ctx.author.guild_permissions.manage_messages:
            await ctx.send("⚠️ You do not have permission to make announcements.")
            return

        if not channel or not message:
            await ctx.send("⚠️ Please mention a channel and provide a message.")
            return

        embed = discord.Embed(title="📢 Announcement", description=message, color=discord.Color.gold())
        await channel.send(embed=embed)
        await ctx.send(f"✅ Announcement sent to {channel.mention}.")
