# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# events.py

from discord import Member, Embed
import bot.config as config
from bot.logger import log_error

def setup(bot):
    """
    Set up the event handlers for the bot.
    """

    # Event for when a new member joins the server
    @bot.event
    async def on_member_join(member: Member):
        """
        Called when a new member joins the server.
        Sends a welcome message in the specified channel.
        """
        specific_channel_id = config.CHANNEL_FOR_MESSAGE
        channel = member.guild.get_channel(specific_channel_id)

        if channel:
            embed = Embed(
                title="Welcome to the Server!",
                description=f"We're excited to have you, {member.mention}! 🎉",
                color=0x00ff00  # Green color
            )
            embed.set_thumbnail(url=member.avatar.url)
            embed.add_field(name="Username", value=f"{member.name}#{member.discriminator}", inline=True)
            embed.add_field(name="Member Count", value=f"{member.guild.member_count}", inline=True)
            embed.set_footer(text="Enjoy your stay!")

            await channel.send(embed=embed)
        else:
            log_error(f"Channel with ID {specific_channel_id} not found. Please check the channel ID.")

    # Event for when a member leaves the server
    @bot.event
    async def on_member_remove(member: Member):
        """
        Called when a member leaves the server.
        Sends a goodbye message in the specified channel.
        """
        specific_channel_id = config.CHANNEL_FOR_MESSAGE
        channel = member.guild.get_channel(specific_channel_id)

        if channel:
            # Create an embed for the goodbye message
            embed = Embed(
                title="We're sad to see you go...",
                description=f"Goodbye, {member.mention}. We hope to see you again soon! 😢",
                color=0xff0000  # Red color to indicate goodbye
            )
            embed.set_thumbnail(url=member.avatar.url)
            embed.add_field(name="Username", value=f"{member.name}#{member.discriminator}", inline=True)
            embed.add_field(name="Member Count", value=f"{member.guild.member_count}", inline=True)
            embed.set_footer(text="Take care!")

            await channel.send(embed=embed)
        else:
            log_error(f"Channel with ID {specific_channel_id} not found. Please check the channel ID.")
