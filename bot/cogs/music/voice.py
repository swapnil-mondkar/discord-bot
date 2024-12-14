# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# bot.cogs.music.voice.py

import discord
import yt_dlp as youtube_dl
import asyncio
from functools import partial
import os
from discord.ext import commands

# A queue to hold song URLs
music_queue = []
current_song = {}

# Configure youtube_dl options
ytdl_format_options = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }],
    'noplaylist': True,
    'quiet': True,
    'outtmpl': 'recording/%(extractor)s/%(id)s.%(ext)s',
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -b:a 192k',
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

def setup(bot):

    # Define the `/join` command
    @bot.command()
    @commands.guild_only()
    async def join(ctx):
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

    # Define the `/leave` command
    @bot.command()
    @commands.guild_only()
    async def leave(ctx):
        """Command to make the bot leave the voice channel."""
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            guild_id = ctx.guild.id
            folder_path = f"recording/{guild_id}"
            
            if os.path.exists(folder_path):
                try:
                    # Remove all files and the folder
                    for file in os.listdir(folder_path):
                        file_path = os.path.join(folder_path, file)
                        os.remove(file_path)
                        print(f"Deleted file: {file_path}")
                    os.rmdir(folder_path)
                    print(f"Deleted folder: {folder_path}")
                except Exception as e:
                    await ctx.send("⚠️ Error cleaning up files!")
                    print(f"Error deleting folder {folder_path}: {e}")

            await ctx.send("👋 Left the voice channel and cleaned up files!")
        else:
            await ctx.send("⚠️ I'm not in a voice channel!")

    # TODO - Swapnil make it better.
    async def ytdl_search(query):
        """Use youtube_dl to extract video info for a given search query."""
        loop = asyncio.get_event_loop()
        try:
            # Run ytdl extraction asynchronously
            info = await loop.run_in_executor(None, partial(ytdl.extract_info, query, download=False))
            return info
        except Exception as e:
            print(f"Error during YouTube search: {e}")
            return None

    async def fetch_youtube_results(query):
        try:
            result = await ytdl_search(query)
            return result
        except Exception as e:
            print(f"Error fetching YouTube results: {e}")
            return None

    # Define the `/play` command
    async def download_audio(url, guild_id, title):
        """Download the audio from YouTube and save it in the 'recording' folder."""
        loop = asyncio.get_event_loop()
        try:
            # Ensure the directory exists
            os.makedirs(f"recording/{guild_id}", exist_ok=True)

            # Adjust the output template to save the file to the correct guild directory
            ytdl_opts = ytdl_format_options.copy()
            ytdl_opts['outtmpl'] = f"recording/{guild_id}/{title}"  # Save to specific guild directory
            ytdl_temp = youtube_dl.YoutubeDL(ytdl_opts)

            # Run the download command asynchronously
            await loop.run_in_executor(None, lambda: ytdl_temp.download([url]))

            # Return the file path after downloading
            return f"recording/{guild_id}/{title}.mp3"
        except Exception as e:
            print(f"Error downloading audio: {e}")
            return None

    # Enqueue a song to the queue and start playback if not already playing
    async def enqueue_song(ctx, file_path, title):
        """Add a song to the queue and start playback if not already playing."""
        music_queue.append({'file_path': file_path, 'title': title})
        if not ctx.voice_client.is_playing():
            await play_next(ctx)

    # Play the downloaded audio
    async def play_audio(ctx, file_path, title):
        """Play the downloaded audio in the voice channel."""
        global current_song
        try:
            # Check if the file exists
            if not os.path.exists(file_path):
                await ctx.send(f"⚠️ File does not exist: {file_path}")
                print(f"File does not exist at: {file_path}")
                return

            # Set the currently playing song
            current_song = {'file_path': file_path, 'title': title}

            # Create an FFmpegPCMAudio source
            audio_source = discord.FFmpegPCMAudio(file_path, executable="ffmpeg")

            def after_playback(error):
                if error:
                    print(f"Error during playback: {error}")

                # Cleanup the file after playback
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                        print(f"Deleted file: {file_path}")
                    except Exception as e:
                        print(f"Error deleting file {file_path}: {e}")

                bot.loop.create_task(play_next(ctx))

            # Play the audio
            ctx.voice_client.play(audio_source, after=after_playback)
            await ctx.send(f"🎵 Now playing: {title}")
        except Exception as e:
            await ctx.send("⚠️ Could not play the song.")
            print(f"Error playing song: {e}")

    # Play the next song in the queue
    async def play_next(ctx):
        """Play the next song in the queue."""
        if not music_queue:
            await ctx.send("🚫 Queue is empty!")
            return

        next_item = music_queue.pop(0)
        if isinstance(next_item, dict):
            file_path = next_item['file_path']
            title = next_item['title']
            await play_audio(ctx, file_path, title)
        else:
            try:
                info = ytdl.extract_info(next_item, download=False)
                if 'entries' in info:
                    info = info['entries'][0]

                file_path = f"recording/{ctx.guild.id}/{info['title']}.mp3"
                title = info.get('title', 'Unknown')
                await play_audio(ctx, file_path, title)
            except Exception as e:
                await ctx.send("⚠️ Could not play the song.")
                print(f"Error playing song: {e}")

    # Adjust the `/play` command to enqueue songs
    @bot.command()
    @commands.guild_only()
    async def play(ctx, *, query):
        if not ctx.voice_client:
            await ctx.invoke(join)

        loading_message = await ctx.send("🔎 Searching and downloading your song...")

        if query.startswith("http://") or query.startswith("https://"):
            # Handle direct URL
            try:
                info = await ytdl_search(query)
                if info:
                    title = info['title']
                    file_path = await download_audio(query, ctx.guild.id, title)
                    if file_path:
                        await enqueue_song(ctx, file_path, title)
                        await loading_message.edit(content=f"✅ Added to queue: {title}")
                    else:
                        await loading_message.edit(content="⚠️ Failed to download the song.")
            except Exception as e:
                await loading_message.edit(content="⚠️ Could not process the URL.")
                print(f"Error processing URL: {e}")
        else:
            # Handle search query
            search_query = f"ytsearch:{query}"
            try:
                search_results = await fetch_youtube_results(search_query)
                if not search_results or 'entries' not in search_results or not search_results['entries']:
                    await loading_message.edit(content="⚠️ No results found!")
                    return

                # Select the first result
                first_result = search_results['entries'][0]
                music_url = first_result['webpage_url']
                title = first_result['title']

                await loading_message.edit(content=f"✅ Downloading song: {title}")
                file_path = await download_audio(music_url, ctx.guild.id, title)
                if file_path:
                    await enqueue_song(ctx, file_path, title)
                    await loading_message.edit(content=f"✅ Added to queue: {title}")
                else:
                    await loading_message.edit(content="⚠️ Failed to download the song.")
            except Exception as e:
                await loading_message.edit(content="⚠️ Could not search for the song.")
                print(f"Error during search: {e}")

    # Define the `/pause` command
    @bot.command()
    @commands.guild_only()
    async def pause(ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("Playback paused!")
        else:
            await ctx.send("Nothing is currently playing!")

    # Define the `/resume` command
    @bot.command()
    @commands.guild_only()
    async def resume(ctx):
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("Playback resumed!")
        else:
            await ctx.send("Playback is not paused!")

    # Define the `/stop` command
    @bot.command()
    @commands.guild_only()
    async def stop(ctx):
        """Stop playback, clean up the current file, and clear the queue."""
        global current_song  # Ensure access to the global variable tracking the current song

        if ctx.voice_client:
            # Stop playback
            ctx.voice_client.stop()
            await ctx.send("⏹️ Playback stopped!")

            # Clean up the current playing file
            if current_song:
                file_path = current_song.get('file_path')
                if file_path and os.path.exists(file_path):
                    try:
                        os.remove(file_path)  # Delete the file
                        print(f"Deleted file after stopping: {file_path}")
                    except Exception as e:
                        print(f"Error deleting file {file_path}: {e}")
                current_song = {}  # Reset the current song tracker

            # Clear the music queue
            music_queue.clear()
            print("Music queue cleared.")
            await ctx.send("🧹 Cleared the music queue!")
        else:
            await ctx.send("🚫 Nothing is currently playing!")

    # Define the `/queue` command
    @bot.command()
    @commands.guild_only()
    async def queue(ctx):
        if music_queue:
            queue_list = "\n".join([f"{idx+1}. {url}" for idx, url in enumerate(music_queue)])
            await ctx.send(f"Current queue:\n{queue_list}")
        else:
            await ctx.send("The queue is empty!")

    # Define the `/skip` command
    @bot.command()
    @commands.guild_only()
    async def skip(ctx):
        """Skip the current playing song and clean up the file."""
        if ctx.voice_client is None or not ctx.voice_client.is_playing():
            await ctx.send("⚠️ No song is currently playing!")
            return

        # Stop the current song
        ctx.voice_client.stop()
        await ctx.send("⏭️ Skipped the current song!")

        # Remove the file of the currently playing song
        if 'current_song' in globals() and current_song:
            file_path = current_song.get('file_path')
            if file_path and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    print(f"Deleted file after skipping: {file_path}")
                except Exception as e:
                    print(f"Error deleting file {file_path}: {e}")

        # Play the next song in the queue, if any
        await play_next(ctx)

    @bot.event
    async def on_voice_state_update(member, before, after):
        """Handle voice state updates to delete guild folders when the bot leaves."""
        # Check if the bot is the one leaving the channel
        if member == bot.user and before.channel is not None and after.channel is None:
            guild_id = member.guild.id
            folder_path = f"recording/{guild_id}"

            if os.path.exists(folder_path):
                try:
                    # Remove all files and the folder
                    await asyncio.sleep(1)
                    for file in os.listdir(folder_path):
                        file_path = os.path.join(folder_path, file)
                        os.remove(file_path)
                        print(f"Deleted file: {file_path}")
                    os.rmdir(folder_path)
                    print(f"Deleted folder: {folder_path}")
                except Exception as e:
                    print(f"Error deleting folder {folder_path}: {e}")
