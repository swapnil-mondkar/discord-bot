# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# stop.py

def setup(bot):

    # Define the `/stoprecord` command to stop recording
    @bot.command()
    async def stoprecord(ctx):
        # Check if the bot is currently in a voice channel and recording
        if ctx.voice_client:
            # Stop the audio capture
            ctx.voice_client.stop()
            await ctx.send("Recording stopped.")
        else:
            await ctx.send("I am not recording.")
