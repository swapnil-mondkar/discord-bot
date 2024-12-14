# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# bot.cogs.admin.scanner.py

from bot.extensions.logger import logger

def setup(bot):

    db = bot.db
    guilds_collection = db["guilds"]

    # scanchannel
    @bot.command()
    async def scanchannel(ctx):
        try:
            # Check if the command is issued in a guild (server)
            if ctx.guild is None:
                await ctx.send("This command can only be used in a server.")
                return

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
    async def scanmember(ctx):
        try:
            # Check if the command is issued in a guild (server)
            if ctx.guild is None:
                await ctx.send("This command can only be used in a server.")
                return

            # Get guild (server) information
            guild_id = ctx.guild.id
            guild_name = ctx.guild.name

            # Fetch all members from the guild
            members = [
                {"member_id": member.id, "member_name": member.name}
                for member in ctx.guild.members
                if not member.bot  # Exclude bot accounts if needed
            ]

            # Prepare the data to store in MongoDB
            guild_data = {
                "guild_id": guild_id,
                "guild_name": guild_name,
                "members": members,  # Add members to the data
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
