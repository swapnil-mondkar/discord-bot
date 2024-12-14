# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# bot.cogs.github.setup.py

import discord
import asyncio
from github import Github
from discord.ui import Button, View
from discord.ext import commands
from datetime import datetime, timedelta

def setup(bot):

    db = bot.db
    guilds_collection = db['guilds']

    @bot.command()
    async def set_github(ctx):
        """Start the process of setting GitHub repository configuration in DMs."""
        if not ctx.guild:
            await ctx.send("This command can only be used in a server.")
            return

        # Notify the user to send the details in DM
        await ctx.send(
            "Please send me the GitHub repository name and token via Direct Message (DM).\n"
            "In the following format:\n"
            "`repo_name: <repo_name>`\n"
            "`token: <your_token>`\n"
            "I will configure it for your server."
        )

        # Ask the user to DM the bot
        try:
            # Wait for the user's DM with both repo_name and token
            def check(msg):
                return msg.author == ctx.author and isinstance(msg.channel, discord.DMChannel)

            # Wait for the message with repo_name
            dm_message = await bot.wait_for('message', check=check, timeout=60.0)

            # Extract repo_name and token from the DM message
            if dm_message.content.startswith('repo_name:') and 'token:' in dm_message.content:
                repo_name = dm_message.content.split('repo_name:')[1].split('token:')[0].strip()
                token = dm_message.content.split('token:')[1].strip()

                # Proceed with the repo_name and token
                guild_id = ctx.guild.id
                created_by = ctx.author.id

                # Structure the new repository data
                new_repo = {
                    "repo_name": repo_name,
                    "token": token,
                    "created_by": created_by
                }

                # Update the guild's document to include the new repository
                guilds_collection.update_one(
                    {"guild_id": guild_id},
                    {"$addToSet": {"github": new_repo}},
                    upsert=True
                )

                await dm_message.author.send("Your GitHub repository has been successfully configured!")
            else:
                await dm_message.author.send(
                    "Invalid format. Please provide both the `repo_name` and `token` in the following format:\n"
                    "`repo_name: <repo_name>`\n"
                    "`token: <your_token>`"
                )
        except asyncio.TimeoutError:
            await ctx.send("You took too long to provide the details. Please try again.")

    @bot.command()
    @commands.guild_only()
    async def show_github(ctx):
        """Show all configured GitHub repositories for the guild."""
        if not ctx.guild:
            await ctx.send("This command can only be used in a server.")
            return

        guild_id = ctx.guild.id
        guild_config = guilds_collection.find_one({"guild_id": guild_id})

        if not guild_config or not guild_config.get("github"):
            await ctx.send("No GitHub repositories are configured for this server.")
            return

        # Retrieve and display the list of repositories
        repos = guild_config["github"]
        repo_list = "Configured GitHub Repositories:\n"
        for repo in repos:
            repo_list += f"Repo: {repo['repo_name']}\n"
            repo_list += f"Created by: <@{repo['created_by']}>\n"
            repo_list += f"Token: {'***REDACTED***'}\n\n"

        await ctx.send(repo_list)

    @bot.command()
    @commands.guild_only()
    async def contributions(ctx):
        """Start the process to select a dynamic date range for contributions."""
        if not ctx.guild:
            await ctx.send("This command can only be used in a server.")
            return

        guild_id = ctx.guild.id
        config = guilds_collection.find_one({"guild_id": guild_id})

        if not config or "github" not in config:
            await ctx.send("GitHub configuration is not set for this server.")
            return

        # Prepare buttons for time range selection (week, month, year)
        time_range_buttons = [
            Button(label="Last Day", custom_id="last_day"),
            Button(label="Last Week", custom_id="last_week"),
            Button(label="Last Month", custom_id="last_month"),
            Button(label="Last Year", custom_id="last_year")
        ]

        time_range_view = View()
        for button in time_range_buttons:
            time_range_view.add_item(button)

        await ctx.send("Please select a time range for the contributions:", view=time_range_view)

        # Wait for the user's time range selection
        def check_time_range(interaction):
            return interaction.user == ctx.author and interaction.data['custom_id'] in ["last_day", "last_week", "last_month", "last_year"]

        try:
            time_range_interaction = await bot.wait_for('interaction', check=check_time_range, timeout=60.0)
            selected_range = time_range_interaction.data['custom_id']
            await time_range_interaction.response.send_message(f"Selected time range: {selected_range.replace('_', ' ').capitalize()}", ephemeral=True)

            # Calculate the date range based on selection
            if selected_range == "last_day":
                start_date = datetime.now() - timedelta(days=1)
                end_date = datetime.now()
            elif selected_range == "last_week":
                start_date = datetime.now() - timedelta(weeks=1)
                end_date = datetime.now()
            elif selected_range == "last_month":
                start_date = datetime.now() - timedelta(weeks=4)
                end_date = datetime.now()
            elif selected_range == "last_year":
                start_date = datetime.now() - timedelta(days=365)
                end_date = datetime.now()

            # Fetch contributions within the selected date range for the selected repositories
            contributions = {}

            for repo in config['github']:
                github = Github(repo['token'])
                repo_instance = github.get_repo(repo['repo_name'])
                contributors = repo_instance.get_contributors()
                repo_contributions = []

                for contributor in contributors:
                    commits = repo_instance.get_commits(author=contributor.login, since=start_date, until=end_date)
                    commit_count = commits.totalCount
                    repo_contributions.append({
                        "author_name": contributor.login,
                        "commits": commit_count
                    })

                if repo_contributions:
                    contributions[repo['repo_name']] = repo_contributions

            if not contributions:
                await ctx.send(f"No contributions between {start_date.strftime('%Y-%m-%d')} and {end_date.strftime('%Y-%m-%d')}.")
                return

            # Prepare the message to send
            contribution_message = f"Contributions from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}:\n"
            
            for repo_name, contribs in contributions.items():
                contribution_message += f"\n**{repo_name}**:\n"
                for contrib in contribs:
                    contribution_message += f"- {contrib['author_name']}: {contrib['commits']} commits\n"
            
            # Split the message if it exceeds the character limit
            MAX_MESSAGE_LENGTH = 2000
            for i in range(0, len(contribution_message), MAX_MESSAGE_LENGTH):
                await ctx.send(contribution_message[i:i+MAX_MESSAGE_LENGTH])

        except asyncio.TimeoutError:
            await ctx.send("You took too long to select the time range. Please try again.")
