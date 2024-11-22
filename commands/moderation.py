# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# moderation.py

import discord
from .logger import log_to_mongo, log_error

def setup(bot):

    # Define the `/kick` command
    @bot.command()
    async def kick(ctx, user: discord.User = None, *, reason: str = None):  # Notice the '*' before 'reason'
        # Check if the bot has the right permission to kick
        if not ctx.author.guild_permissions.kick_members:
            await ctx.send("⚠️ You do not have permission to kick members.")
            return

        if not user:
            await ctx.send("⚠️ Please mention the user you want to kick.")
            return

        try:
            # Fetch the member object from the guild
            member = ctx.guild.get_member(user.id)
            
            if member is None:
                await ctx.send(f"⚠️ {user.name} is not a member of this server.")
                return
            
            # Send a DM to the user with the reason for the kick
            try:
                dm_message = f"Hello {user.name},\n\nYou have been kicked from the server '{ctx.guild.name}'."
                dm_message += f"\nReason: {reason if reason else 'No reason provided.'}"
                await user.send(dm_message)
            except discord.Forbidden:
                # If the user has DMs disabled, this will be caught
                await ctx.send(f"⚠️ Could not send a DM to {user.name}. They may have DMs disabled.")

            # Kick the mentioned member
            await member.kick(reason=reason)
            await ctx.send(f"✅ {user.name} has been kicked from the server.", delete_after=5)

            # Log the kick action
            # log_to_mongo(
            #     author_name=ctx.author.name,
            #     author_id=str(ctx.author.id),
            #     action="kick",
            #     target_name=user.name,
            #     target_id=str(user.id),
            #     reason=reason if reason else "No reason provided",
            #     channel_name=ctx.channel.name,
            # )

        except discord.Forbidden:
            await ctx.send("⚠️ I do not have permission to kick this user.")
        except discord.HTTPException:
            await ctx.send("⚠️ An error occurred while trying to kick the user.")
        except Exception as e:
            await ctx.send("⚠️ Something went wrong.")
            log_error(f"Error in kicking user: {e}")

    # Define the `/ban` command
    @bot.command()
    async def ban(ctx, user: discord.User = None, *, reason: str = None):  # Using '*' to capture the reason
        # Check if the bot has the right permission to ban
        if not ctx.author.guild_permissions.ban_members:
            await ctx.send("⚠️ You do not have permission to ban members.")
            return

        if not user:
            await ctx.send("⚠️ Please mention the user you want to ban.")
            return

        try:
            # Fetch the member object from the guild
            member = ctx.guild.get_member(user.id)

            if member is None:
                await ctx.send(f"⚠️ {user.name} is not a member of this server.")
                return
            
            # Send a DM to the user with the reason for the ban
            try:
                dm_message = f"Hello {user.name},\n\nYou have been banned from the server '{ctx.guild.name}'."
                dm_message += f"\nReason: {reason if reason else 'No reason provided.'}"
                await user.send(dm_message)
            except discord.Forbidden:
                # If the user has DMs disabled, this will be caught
                await ctx.send(f"⚠️ Could not send a DM to {user.name}. They may have DMs disabled.")

            # Ban the mentioned member
            await member.ban(reason=reason)
            await ctx.send(f"✅ {user.name} has been banned from the server.", delete_after=5)

            # Log the ban action
            # log_to_mongo(
            #     author_name=ctx.author.name,
            #     author_id=str(ctx.author.id),
            #     action="ban",
            #     target_name=user.name,
            #     target_id=str(user.id),
            #     reason=reason if reason else "No reason provided",
            #     channel_name=ctx.channel.name,
            # )

        except discord.Forbidden:
            await ctx.send("⚠️ I do not have permission to ban this user.")
        except discord.HTTPException:
            await ctx.send("⚠️ An error occurred while trying to ban the user.")
        except Exception as e:
            await ctx.send("⚠️ Something went wrong.")
            log_error(f"Error in banning user: {e}")
