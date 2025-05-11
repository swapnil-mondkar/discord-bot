# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# bot.cogs.guild.info.py

from discord.ext import commands

def setup(bot):
    db = bot.db
    guild_collection = db['guild']

    @bot.command()
    @commands.guild_only()
    async def guild_info(ctx):
        guild = ctx.guild  # The current guild (server) object

        # Collecting basic guild information
        guild_name = guild.name
        guild_id = guild.id
        owner = guild.owner
        member_count = guild.member_count
        created_at = guild.created_at.strftime("%Y-%m-%d %H:%M:%S")  # Format creation date

        # Creating an embed for better presentation
        embed = commands.Embed(
            title=f"Information for {guild_name}",
            color=0x3498db  # Blue color
        )
        embed.add_field(name="Guild Name", value=guild_name, inline=False)
        embed.add_field(name="Guild ID", value=guild_id, inline=False)
        embed.add_field(name="Owner", value=f"{owner} ({owner.id})", inline=False)
        embed.add_field(name="Member Count", value=member_count, inline=False)
        embed.add_field(name="Created At", value=created_at, inline=False)

        # Optionally store guild data in the database
        guild_data = {
            "guild_id": guild_id,
            "guild_name": guild_name,
            "owner_id": owner.id,
            "member_count": member_count,
            "created_at": created_at
        }
        guild_collection.update_one(
            {"guild_id": guild_id}, {"$set": guild_data}, upsert=True
        )

        # Send the embed as a response
        await ctx.send(embed=embed)
