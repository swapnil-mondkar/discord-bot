# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# bot.cogs.moderation.role.py

import asyncio
import discord
from discord.ext import commands
from bot.extensions.logger import logger

def setup(bot):

    # Define the `/addrole` command
    @bot.command()
    @commands.guild_only()
    async def addrole(ctx, user: discord.Member = None, *, role_name: str = None):
        if not ctx.author.guild_permissions.manage_roles:
            await ctx.send("⚠️ You do not have permission to manage roles.")
            return

        if not user or not role_name:
            await ctx.send("⚠️ Please mention a user and specify a role.")
            return

        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if not role:
            await ctx.send(f"⚠️ Role '{role_name}' not found.")
            return

        await user.add_roles(role)
        await ctx.send(f"✅ {role_name} role has been assigned to {user.name}.")

    # Define the `/removerole` command
    @bot.command()
    @commands.guild_only()
    async def removerole(ctx, user: discord.Member = None, *, role_name: str = None):
        if not ctx.author.guild_permissions.manage_roles:
            await ctx.send("⚠️ You do not have permission to manage roles.")
            return

        if not user or not role_name:
            await ctx.send("⚠️ Please mention a user and specify a role.")
            return

        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if not role:
            await ctx.send(f"⚠️ Role '{role_name}' not found.")
            return

        await user.remove_roles(role)
        await ctx.send(f"✅ {role_name} role has been removed from {user.name}.")

    # Define the `/temprole` command
    @bot.command()
    @commands.guild_only()
    async def temprole(ctx, user: discord.Member = None, role_name: str = None, duration: int = 0):
        if not ctx.author.guild_permissions.manage_roles:
            await ctx.send("⚠️ You do not have permission to manage roles.")
            return

        if not user or not role_name or duration <= 0:
            await ctx.send("⚠️ Please mention a valid user, role, and duration (in seconds).")
            return

        try:
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            if not role:
                await ctx.send(f"⚠️ Role '{role_name}' not found.")
                return

            await user.add_roles(role)
            await ctx.send(f"✅ {role_name} has been assigned to {user.name} for {duration} seconds.")

            await asyncio.sleep(duration)
            if role in user.roles:
                await user.remove_roles(role)
                await ctx.send(f"✅ {role_name} has been removed from {user.name}.")
        except Exception as e:
            await ctx.send("⚠️ Something went wrong.")
            logger.log_error(f"Error in temprole command: {e}")
