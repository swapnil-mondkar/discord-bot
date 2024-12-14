# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# bot.cogs.moderation.slowdown.py

import discord
from discord.ext import commands
from bot.extensions.logger import logger

def setup(bot):

    # Define the `/lockdown` command
    @bot.command()
    @commands.guild_only()
    async def lockdown(ctx, channel: discord.TextChannel = None):
        if not ctx.author.guild_permissions.manage_channels:
            await ctx.send("⚠️ You do not have permission to lockdown channels.")
            return

        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(f"🔒 {channel.name} has been locked down.")

    # Define the `/unlock` command
    @bot.command()
    @commands.guild_only()
    async def unlock(ctx, channel: discord.TextChannel = None):
        if not ctx.author.guild_permissions.manage_channels:
            await ctx.send("⚠️ You do not have permission to unlock channels.")
            return

        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = None  # Reset to default
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(f"🔓 {channel.name} has been unlocked.")

    # Define the `/slowmode` command
    @bot.command()
    @commands.guild_only()
    async def slowmode(ctx, seconds: int = 0):
        if not ctx.author.guild_permissions.manage_channels:
            await ctx.send("⚠️ You do not have permission to set slowmode.")
            return

        if seconds < 0:
            await ctx.send("⚠️ Slowmode duration must be 0 or greater.")
            return

        await ctx.channel.edit(slowmode_delay=seconds)
        if seconds == 0:
            await ctx.send(f"✅ Slowmode has been disabled for {ctx.channel.name}.")
        else:
            await ctx.send(f"✅ Slowmode has been set to {seconds} seconds for {ctx.channel.name}.")
