# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# bot.cogs.admin.scanner.py

from discord.ext import commands
from bot.extensions.logger import logger

def setup(bot):

    db = bot.db
    guilds_collection = db["guilds"]

    # scanchannel
    @bot.command()
    @commands.guild_only()
    async def scanchannel(ctx):
        try:
            # Get guild (server) information
            guild_id = ctx.guild.id
            guild_name = ctx.guild.name

            # Separate text and voice channels
            text_channels = [
                {"channel_id": channel.id, "channel_name": channel.name}
                for channel in ctx.guild.text_channels
            ]
            voice_channels = [
                {"channel_id": channel.id, "channel_name": channel.name}
                for channel in ctx.guild.voice_channels
            ]

            # Prepare the data to store in MongoDB
            guild_data = {
                "guild_id": guild_id,
                "guild_name": guild_name,
                "text_channels": text_channels,
                "voice_channels": voice_channels,
            }

            # Upsert the guild data into MongoDB (update if exists, insert if not)
            guilds_collection.update_one(
                {"guild_id": guild_id},
                {"$set": guild_data},
                upsert=True
            )

            # Send confirmation message
            await ctx.send(
                f"Scanned {len(text_channels)} text channels and {len(voice_channels)} voice channels in '{guild_name}' and stored in the database."
            )

        except Exception as e:
            await ctx.send("⚠️ Something went wrong while scanning channels.")
            logger.log_error(f"Error in scanchannel: {e}")

    # scanmember
    @bot.command()
    @commands.guild_only()
    async def scanmember(ctx):
        try:
            # Get guild (server) information
            guild_id = ctx.guild.id
            guild_name = ctx.guild.name

            # Fetch all members from the guild
            members = [
                {"member_id": member.id, "member_name": member.name}
                for member in ctx.guild.members
                if not member.bot
            ]

            # Prepare the data to store in MongoDB
            guild_data = {
                "guild_id": guild_id,
                "guild_name": guild_name,
                "members": members,
            }

            # Upsert the guild data into MongoDB (update if exists, insert if not)
            guilds_collection.update_one(
                {"guild_id": guild_id},
                {"$set": guild_data},
                upsert=True
            )

            # Send confirmation message
            await ctx.send(
                f"Scanned {len(members)} members in '{guild_name}' and stored in the database."
            )

        except Exception as e:
            await ctx.send("⚠️ Something went wrong while scanning members.")
            logger.log_error(f"Error in scanmember: {e}")

    # scanroles
    @bot.command()
    @commands.guild_only()
    async def scanroles(ctx):
        try:
            # Get guild (server) information
            guild_id = ctx.guild.id
            guild_name = ctx.guild.name

            # Initialize list to hold role data
            roles = []

            # Fetch all roles from the guild and process their permissions
            for role in ctx.guild.roles:
                # Retrieve all permissions for this role
                role_permissions = {
                    "administrator": role.permissions.administrator,
                    "manage_roles": role.permissions.manage_roles,
                    "manage_channels": role.permissions.manage_channels,
                    "kick_members": role.permissions.kick_members,
                    "ban_members": role.permissions.ban_members,
                    "manage_guild": role.permissions.manage_guild,
                    "view_audit_log": role.permissions.view_audit_log,
                    "send_messages": role.permissions.send_messages,
                    "manage_messages": role.permissions.manage_messages,
                    "read_messages": role.permissions.read_messages,
                    "mention_everyone": role.permissions.mention_everyone,
                    "embed_links": role.permissions.embed_links,
                    "attach_files": role.permissions.attach_files,
                    "read_message_history": role.permissions.read_message_history,
                    "mention_everyone": role.permissions.mention_everyone,
                    "use_external_emojis": role.permissions.use_external_emojis,
                    "add_reactions": role.permissions.add_reactions,
                    "manage_nicknames": role.permissions.manage_nicknames,
                    "manage_emojis": role.permissions.manage_emojis,
                    "manage_webhooks": role.permissions.manage_webhooks
                }

                # Add role data to list
                roles.append({
                    "role_id": role.id,
                    "role_name": role.name,
                    "role_permissions": role_permissions,
                })

            # Prepare the data to store in MongoDB
            guild_data = {
                "guild_id": guild_id,
                "guild_name": guild_name,
                "roles": roles,
            }

            # Upsert the guild data into MongoDB (update if exists, insert if not)
            guilds_collection.update_one(
                {"guild_id": guild_id},
                {"$set": guild_data},
                upsert=True
            )

            # Send confirmation message
            await ctx.send(
                f"Scanned {len(roles)} roles in '{guild_name}' and stored in the database."
            )

        except Exception as e:
            # Send user-friendly error message
            await ctx.send("⚠️ Something went wrong while scanning roles.")

            # Log the error with detailed information
            logger.log_error(f"Error in scanroles command in guild {ctx.guild.name} (ID: {ctx.guild.id}): {e}")
