# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# bot.cogs.moderation.mutewarn.py

import discord
from discord.ext import commands
from bot.extensions.logger import logger

def setup(bot):

    # Define the `/mute` command
    @bot.command()
    @commands.guild_only()
    async def mute(ctx, user: discord.Member = None, *, reason: str = None):
        if not ctx.author.guild_permissions.manage_roles:
            await ctx.send("⚠️ You do not have permission to mute members.")
            return

        if not user:
            await ctx.send("⚠️ Please mention the user you want to mute.")
            return

        try:
            muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
            if not muted_role:
                muted_role = await ctx.guild.create_role(name="Muted")
                for channel in ctx.guild.channels:
                    await channel.set_permissions(muted_role, speak=False, send_messages=False, add_reactions=False)

            if muted_role in user.roles:
                await ctx.send(f"⚠️ {user.name} is already muted.")
                return

            await user.add_roles(muted_role, reason=reason)
            await ctx.send(f"✅ {user.name} has been muted. Reason: {reason if reason else 'No reason provided.'}")

        except discord.Forbidden:
            await ctx.send("⚠️ I do not have permission to mute this user.")
        except discord.HTTPException:
            await ctx.send("⚠️ An error occurred while trying to mute the user.")
        except Exception as e:
            await ctx.send("⚠️ Something went wrong.")
            logger.log_error(f"Error in muting user: {e}")

    # Define the `/unmute` command
    @bot.command()
    @commands.guild_only()
    async def unmute(ctx, user: discord.Member = None):
        if not ctx.author.guild_permissions.manage_roles:
            await ctx.send("⚠️ You do not have permission to unmute members.")
            return

        if not user:
            await ctx.send("⚠️ Please mention the user you want to unmute.")
            return

        try:
            muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
            if not muted_role or muted_role not in user.roles:
                await ctx.send(f"⚠️ {user.name} is not muted.")
                return

            await user.remove_roles(muted_role)
            await ctx.send(f"✅ {user.name} has been unmuted.")

        except discord.Forbidden:
            await ctx.send("⚠️ I do not have permission to unmute this user.")
        except discord.HTTPException:
            await ctx.send("⚠️ An error occurred while trying to unmute the user.")
        except Exception as e:
            await ctx.send("⚠️ Something went wrong.")
            logger.log_error(f"Error in unmuting user: {e}")

    # Define the `/warn` command
    @bot.command()
    @commands.guild_only()
    async def warn(ctx, user: discord.Member = None, *, reason: str = None):
        if not ctx.author.guild_permissions.manage_messages:
            await ctx.send("⚠️ You do not have permission to warn members.")
            return

        if not user:
            await ctx.send("⚠️ Please mention the user you want to warn.")
            return

        reason = reason if reason else "No reason provided."
        # Log warning to MongoDB or any database
        # log_to_mongo(user_id=str(user.id), action="warn", reason=reason)
        await ctx.send(f"⚠️ {user.name} has been warned. Reason: {reason}")

    # Define the `/warnings` command
    @bot.command()
    @commands.guild_only()
    async def warnings(ctx, user: discord.Member = None):
        if not ctx.author.guild_permissions.manage_messages:
            await ctx.send("⚠️ You do not have permission to view warnings.")
            return

        if not user:
            await ctx.send("⚠️ Please mention the user whose warnings you want to view.")
            return

        # Fetch warnings from MongoDB or any database
        # warnings = fetch_warnings(user_id=str(user.id))
        warnings = ["Example Warning 1", "Example Warning 2"]  # Placeholder
        if warnings:
            warning_list = "\n".join([f"{idx+1}. {warning}" for idx, warning in enumerate(warnings)])
            await ctx.send(f"⚠️ {user.name}'s warnings:\n{warning_list}")
        else:
            await ctx.send(f"✅ {user.name} has no warnings.")
