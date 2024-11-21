# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# scanmember.py

from .logger import log_to_mongo, log_error
from mongo import connect_mongo

db = connect_mongo()
guilds_collection = db["guilds"]

def setup(bot):

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
            log_error(f"Error in scanmember: {e}")
