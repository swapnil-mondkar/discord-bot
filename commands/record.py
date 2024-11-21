# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# record.py

from discord import FFmpegPCMAudio

def setup(bot):

    # Define the `/record` command to start recording
    @bot.command()
    async def record(ctx):
        # Ensure the bot is connected to a voice channel
        if not ctx.voice_client:
            await ctx.send("I need to join a voice channel first. Use /joinvoice.")
            return

        # Start recording audio (ffmpeg needs to be installed and available in your system's PATH)
        try:
            # Start capturing the audio
            ffmpeg_options = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                'options': '-vn'
            }
            audio_source = FFmpegPCMAudio('input_audio_stream', **ffmpeg_options)

            # Play the audio source in the voice channel (this captures the input)
            ctx.voice_client.play(audio_source, after=lambda e: print('done', e))

            # Send a message indicating that recording has started
            await ctx.send("Recording started...")
        except Exception as e:
            await ctx.send("⚠️ Failed to record.")
            print(f"Error recording voice: {e}")
