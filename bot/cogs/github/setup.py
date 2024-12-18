# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# bot.cogs.github.setup.py

import discord
import asyncio
import requests
from github import Github
from discord.ui import Button, View
from discord.ext import commands
from datetime import datetime, timedelta

def setup(bot):

    db = bot.db
    users_collection = db['users']

    @bot.command()
    async def set_github(ctx, github_username):
        """Command to fetch GitHub data and store in MongoDB."""
        # Check if the user has a GitHub token stored
        user_data = users_collection.find_one({"discord_id": ctx.author.id})
        headers = {}

        if user_data and "github" in user_data and "token" in user_data["github"]:
            headers = {"Authorization": f"token {user_data['github']['token']}"}

        # Fetch GitHub user profile
        url = f"https://api.github.com/users/{github_username}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            user_profile = {
                "github_username": data.get("login"),
                "profile_url": data.get("html_url"),
                "name": data.get("name"),
                "bio": data.get("bio"),
                "public_repos": data.get("public_repos"),
                "followers": data.get("followers"),
                "following": data.get("following")
            }

            # Fetch repositories (including private if token is present)
            repos_url = f"https://api.github.com/user/repos"
            repos_response = requests.get(repos_url, headers=headers)
            repos_data = repos_response.json() if repos_response.status_code == 200 else []
            
            # Add repositories to the user's profile
            user_profile["repos"] = [{"name": repo["name"], "private": repo["private"], "html_url": repo["html_url"]} for repo in repos_data]

            # Insert or update the user profile in MongoDB
            users_collection.update_one(
                {"discord_id": ctx.author.id},
                {
                    "$set": {f"github.{key}": value for key, value in user_profile.items()}
                },
                upsert=True
            )

            await ctx.send(f"GitHub profile for **{github_username}** linked successfully!")
            if not headers:
                await ctx.send(
                    "Only public repositories have been fetched. "
                    "If you want to fetch private repositories too, please run `!github_token token` in a private message to me, and run this command again."
                )
        else:
            await ctx.send(f"Could not fetch GitHub profile for **{github_username}**. Please check the username or ensure your token is valid.")

    @bot.command()
    async def github_token(ctx, token: str):
        """Store GitHub personal access token (PAT) securely in MongoDB under the 'github' field."""
        # Check if the command is sent in a DM channel
        if isinstance(ctx.channel, discord.DMChannel):
            # Store the token securely in MongoDB for the user
            users_collection.update_one(
                {"discord_id": ctx.author.id},
                {"$set": {"github.token": token}},
                upsert=True
            )
            await ctx.send("Your GitHub token has been securely stored!")
        else:
            await ctx.send("Please send this command as a private message (DM) for security.")

    @bot.command()
    @commands.guild_only()
    async def show_github(ctx):
        """Show the GitHub profile(s) configured by the user."""
        # Find the user data from the MongoDB collection
        user_data = users_collection.find_one({"discord_id": ctx.author.id})

        if user_data and "github" not in user_data:
            await ctx.send("You haven't configured any GitHub profile yet. Use `!set_github <username>` to link your GitHub profile.")
            return

        # Retrieve and display the user's GitHub profiles
        profile = user_data["github"]
        profile_list = f"GitHub Profiles Linked by **{ctx.author}**:\n"
        profile_list += f"**Name**: {profile.get('name', 'N/A')}\n"
        profile_list += f"**Username**: {profile.get('github_username', 'N/A')}\n"
        profile_list += f"**Profile URL**: {profile.get('profile_url', 'N/A')}\n"
        profile_list += f"**Followers**: {profile.get('followers', 'N/A')}\n"
        profile_list += f"**Following**: {profile.get('following', 'N/A')}\n"

        await ctx.send(profile_list)

    @bot.command()
    @commands.guild_only()
    async def contributions(ctx):
        """Start the process to select a dynamic date range for contributions."""
        config = users_collection.find_one({"discord_id": ctx.author.id})

        if not config or "github" not in config or "token" not in config['github'] or "repos" not in config['github']:
            await ctx.send("GitHub configuration is incomplete or missing for your account.")
            return

        # Prepare buttons for time range selection
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

        def check_time_range(interaction):
            return interaction.user == ctx.author and interaction.data['custom_id'] in ["last_day", "last_week", "last_month", "last_year"]

        try:
            # Wait for the user's time range selection
            time_range_interaction = await bot.wait_for('interaction', check=check_time_range, timeout=120.0)
            selected_range = time_range_interaction.data['custom_id']
            await time_range_interaction.response.send_message(f"Selected time range: {selected_range.replace('_', ' ').capitalize()}", ephemeral=True)

            # Calculate the date range based on selection
            if selected_range == "last_day":
                start_date = datetime.now() - timedelta(days=1)
            elif selected_range == "last_week":
                start_date = datetime.now() - timedelta(weeks=1)
            elif selected_range == "last_month":
                start_date = datetime.now() - timedelta(weeks=4)
            elif selected_range == "last_year":
                start_date = datetime.now() - timedelta(days=365)

            end_date = datetime.now()

            # Fetch contributions
            contributions = {}
            github = Github(config['github']['token'])

            for repo in config['github']['repos']:
                try:
                    repo_instance = github.get_repo(config['github']['github_username'] + '/' + repo['name'])
                    contributors = repo_instance.get_contributors()
                    repo_contributions = []

                    for contributor in contributors:
                        commits = repo_instance.get_commits(author=contributor.login, since=start_date, until=end_date)
                        repo_contributions.append({
                            "author_name": contributor.login,
                            "commits": commits.totalCount
                        })

                    if repo_contributions:
                        contributions[repo['name']] = repo_contributions

                except Exception as e:
                    await ctx.send(f"Error fetching contributions for '{repo['name']}': {str(e)}")
                    continue

            if not contributions:
                await ctx.send(f"No contributions found between {start_date.strftime('%Y-%m-%d')} and {end_date.strftime('%Y-%m-%d')}.")
                return

            # Prepare the contribution message
            contribution_message = f"Contributions from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}:\n"
            for repo_name, contribs in contributions.items():
                contribution_message += f"\n**{repo_name}**:\n"
                for contrib in contribs:
                    contribution_message += f"- {contrib['author_name']}: {contrib['commits']} commits\n"

            # Split and send the message if it exceeds the limit
            MAX_MESSAGE_LENGTH = 2000
            for i in range(0, len(contribution_message), MAX_MESSAGE_LENGTH):
                await ctx.send(contribution_message[i:i + MAX_MESSAGE_LENGTH])

        except asyncio.TimeoutError:
            await ctx.send("You took too long to select the time range. Please try again.")
