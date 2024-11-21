# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# command.py

import discord
from .logger import log_to_mongo, log_error
from mongo import connect_mongo

db = connect_mongo()
commands_collection = db["commands"]

def setup(bot):

    @bot.command()
    async def commands(ctx):
        try:
            # Fetch all commands from MongoDB
            commands_list = list(commands_collection.find())  # Convert Cursor to a list

            if len(commands_list) == 0:  # Check if the list is empty
                await ctx.send("No commands available right now.")
                return

            # Format the commands into a list
            embed = discord.Embed(
                title="Available Commands",
                description="Here's a list of all the commands you can use:",
                color=discord.Color.blue()
            )

            for command in commands_list:
                embed.add_field(
                    name=f"**{command['name']}**",
                    value=f"**Example:** `{command['example']}`\n**Description:** {command['description']}",
                    inline=False
                )

            # Send the formatted list to the user
            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send("⚠️ Something went wrong while fetching commands.")
            print(f"Error fetching commands: {e}")
