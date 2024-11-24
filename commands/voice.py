# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# connect.py

import discord
import yt_dlp as youtube_dl

# A queue to hold song URLs
music_queue = []

# Configure youtube_dl options
ytdl_format_options = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'noplaylist': True,  # Ensure only a single track is fetched
    'quiet': True,       # Suppress unnecessary logs
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -b:a 192k',
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

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

    # Define the `/play` command
    @bot.command()
    async def play(ctx, *, url):
        if not ctx.voice_client:
            await ctx.invoke(connect)

        # Add the song to the queue
        music_queue.append(url)
        await ctx.send(f"Added to queue: {url}")

        # Play if nothing is currently playing
        if not ctx.voice_client.is_playing():
            await play_next(ctx)

    async def play_next(ctx):
        if music_queue:
            url = music_queue.pop(0)
            try:
                info = ytdl.extract_info(url, download=False)
                if 'entries' in info:  # Handle playlists
                    info = info['entries'][0]

                audio_source = discord.FFmpegPCMAudio(info['url'], **ffmpeg_options)
                ctx.voice_client.play(audio_source, after=lambda e: bot.loop.create_task(play_next(ctx)))
                await ctx.send(f"Now playing: {info.get('title', 'Unknown')}")
            except Exception as e:
                await ctx.send("⚠️ Could not play the song.")
                print(f"Error playing song: {e}")
        else:
            await ctx.send("Queue is empty!")

    # Define the `/pause` command
    @bot.command()
    async def pause(ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("Playback paused!")
        else:
            await ctx.send("Nothing is currently playing!")

    # Define the `/resume` command
    @bot.command()
    async def resume(ctx):
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("Playback resumed!")
        else:
            await ctx.send("Playback is not paused!")

    # Define the `/stop` command
    @bot.command()
    async def stop(ctx):
        if ctx.voice_client:
            ctx.voice_client.stop()
            await ctx.send("Playback stopped!")
        else:
            await ctx.send("Nothing is currently playing!")

    # Define the `/queue` command
    @bot.command()
    async def queue(ctx):
        if music_queue:
            queue_list = "\n".join([f"{idx+1}. {url}" for idx, url in enumerate(music_queue)])
            await ctx.send(f"Current queue:\n{queue_list}")
        else:
            await ctx.send("The queue is empty!")
