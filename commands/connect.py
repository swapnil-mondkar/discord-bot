# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# connect.py


def setup(bot):

    # Define the `/connect` command
    @bot.command()
    async def connect(ctx):
        # Check if the command was run in a voice channel
        if ctx.author.voice:
            # Get the voice channel the user is in
            channel = ctx.author.voice.channel
            
            # Try to connect the bot to the channel
            try:
                await channel.connect()
                await ctx.send(f"Joined {channel.name}!")
            except Exception as e:
                await ctx.send("⚠️ Could not join the voice channel.")
                print(f"Error joining voice channel: {e}")
        else:
            await ctx.send("You need to join a voice channel first!")
