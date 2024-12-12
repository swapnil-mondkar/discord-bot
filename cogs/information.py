# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# cogs/info.py

import discord
from bot.logger import log_to_mongo, log_error

def setup(bot):

    # Define the `/userinfo` command
    @bot.command()
    async def userinfo(ctx, user: discord.Member = None):
        user = user or ctx.author
        embed = discord.Embed(title="User Info", color=discord.Color.blue())
        embed.set_thumbnail(url=user.avatar.url)
        embed.add_field(name="Username", value=user.name, inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Joined Server", value=user.joined_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Account Created", value=user.created_at.strftime("%Y-%m-%d"), inline=True)
        roles = [role.mention for role in user.roles if role != ctx.guild.default_role]
        embed.add_field(name="Roles", value=", ".join(roles) if roles else "None", inline=False)
        await ctx.send(embed=embed)

    # Define the `/serverinfo` command
    @bot.command()
    async def serverinfo(ctx):
        guild = ctx.guild
        embed = discord.Embed(title=f"Server Info - {guild.name}", color=discord.Color.green())
        embed.set_thumbnail(url=guild.icon.url)
        embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Created At", value=guild.created_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Region", value=str(guild.region), inline=True)
        embed.add_field(name="Channels", value=len(guild.channels), inline=True)
        await ctx.send(embed=embed)
