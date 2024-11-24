# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# voice.py

import discord
import yt_dlp as youtube_dl
import asyncio
import functools

# A queue to hold song URLs
music_queue = []

# Configure youtube_dl options
ytdl_format_options = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
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

    # TODO - Swapnil make it better.
    async def fetch_youtube_results(query):
        try:
            loop = asyncio.get_event_loop()
            ytdl_search = functools.partial(ytdl.extract_info, query, download=False)
            return await loop.run_in_executor(None, ytdl_search)
        except Exception as e:
            print(f"Error during YouTube search: {e}")
            return None

    # Define the `/play` command
    @bot.command()
    async def play(ctx, *, query):
        if not ctx.voice_client:
            await ctx.invoke(connect)

        loading_message = await ctx.send("🔎 Searching for your song...")

        if query.startswith("http://") or query.startswith("https://"):
            # Directly add URL to the queue
            music_queue.append(query)
            await loading_message.edit(content=f"✅ Added to queue: {query}")
        else:
            # Asynchronous search
            search_query = f"ytsearch3:{query}"
            search_results = await fetch_youtube_results(search_query)

            if not search_results or 'entries' not in search_results or not search_results['entries']:
                await loading_message.edit(content="⚠️ No results found!")
                return

            search_results = search_results['entries']

            result_message = "**Search results:**\n"
            for idx, video in enumerate(search_results, 1):
                title = video['title']
                duration = video.get('duration', 'Unknown')
                result_message += f"{idx}. {title} ({duration} seconds)\n"
            result_message += "\nType the number of the song you want to play (e.g., `1`)."

            await loading_message.edit(content=result_message)

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()

            try:
                response = await bot.wait_for('message', check=check, timeout=20)
                selection = int(response.content)

                if 1 <= selection <= len(search_results):
                    selected_video = search_results[selection - 1]
                    music_queue.append(selected_video['webpage_url'])
                    await ctx.send(f"✅ Added to queue: {selected_video['title']}")
                else:
                    await ctx.send("⚠️ Invalid selection!")
            except asyncio.TimeoutError:
                await ctx.send("⚠️ You took too long to respond. Please try again.")

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

    # Define the `/skip` command
    @bot.command()
    async def skip(ctx):
        """Skip the current playing song."""
        if ctx.voice_client is None or not ctx.voice_client.is_playing():
            await ctx.send("⚠️ No song is currently playing!")
            return

        # Stop the current song
        ctx.voice_client.stop()
        await ctx.send("⏭️ Skipped the current song!")

        # Play the next song in the queue, if any
        await play_next(ctx)