# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# bot.cogs.github.leaderboard.py

from discord.ext import commands
from github import Github
from collections import defaultdict

def setup(bot):

    db = bot.db
    users_collection = db['users']

    @bot.command()
    @commands.guild_only()
    async def leaderboard(ctx):
        """Display a leaderboard of contributors across all repositories."""
        
        # Fetch user configuration from the database
        config = users_collection.find_one({"discord_id": ctx.author.id})

        if not config or "github" not in config:
            await ctx.send("GitHub configuration is not set for this server.")
            return

        github_token = config['github']['token']
        repositories = config['github'].get('repos', [])
        
        if not repositories:
            await ctx.send("No repositories linked to your GitHub configuration.")
            return

        github = Github(github_token)
        contributor_data = defaultdict(int)  # Dictionary to store commit counts per user

        # Fetch contributions for each repository
        try:
            for repo in repositories:
                repo_name = config['github']['github_username'] + '/' + repo.get('name')
                if not repo_name:
                    continue

                try:
                    repo_instance = github.get_repo(repo_name)
                    contributors = repo_instance.get_contributors()

                    for contributor in contributors:
                        contributor_data[contributor.login] += contributor.contributions

                except Exception as e:
                    await ctx.send(f"Error fetching contributions for '{repo_name}': {e}")
                    continue

            # Sort contributors by total commits in descending order
            sorted_contributors = sorted(contributor_data.items(), key=lambda x: x[1], reverse=True)

            if not sorted_contributors:
                await ctx.send("No contributions found for the linked repositories.")
                return

            # Prepare the leaderboard message
            leaderboard_message = "**GitHub Contributor Leaderboard**\n\n"
            for rank, (username, commits) in enumerate(sorted_contributors[:10], start=1):  # Top 10 contributors
                leaderboard_message += f"**#{rank}** {username}: {commits} commits\n"

            await ctx.send(leaderboard_message)

        except Exception as e:
            await ctx.send(f"An error occurred while fetching the leaderboard: {e}")
