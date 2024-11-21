# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# disconnect.py

def setup(bot):

    # Define the `/disconnect` command
    @bot.command()
    async def disconnect(ctx):
        # Check if the bot is connected to a voice channel
        if ctx.voice_client:
            try:
                # Disconnect the bot from the voice channel
                await ctx.voice_client.disconnect()
                await ctx.send("Left the voice channel!")
            except Exception as e:
                await ctx.send("⚠️ Could not leave the voice channel.")
                print(f"Error leaving voice channel: {e}")
        else:
            await ctx.send("I am not connected to any voice channel!")
