# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# bot.cogs.github.stats.py

import requests
from datetime import datetime, timedelta
from discord.ext import commands
from github import Github

def setup(bot):

    db = bot.db
    users_collection = db['users']

    @bot.command()
    @commands.guild_only()
    async def repo_stats(ctx):
        """Show stats for each linked GitHub repository."""
        config = users_collection.find_one({"discord_id": ctx.author.id})

        if not config or "github" not in config:
            await ctx.send("GitHub configuration is not set for this user.")
            return

        github_token = config['github']['token']
        repositories = config['github'].get('repos', [])

        if not repositories:
            await ctx.send("No repositories linked to your GitHub configuration.")
            return

        github = Github(github_token)
        stats_message = "**Repository Stats**\n\n"

        try:
            for repo in repositories:
                repo_name = config['github']['github_username'] + '/' + repo.get('name')
                if not repo_name:
                    continue

                repo_instance = github.get_repo(repo_name)
                stats_message += f"**{repo_name}**\n"
                stats_message += f"- 🌟 Stars: {repo_instance.stargazers_count}\n"
                stats_message += f"- 🍴 Forks: {repo_instance.forks_count}\n"
                stats_message += f"- 🐛 Open Issues: {repo_instance.open_issues_count}\n"
                stats_message += f"- 👀 Watchers: {repo_instance.watchers_count}\n\n"

            await ctx.send(stats_message)

        except Exception as e:
            await ctx.send(f"Error fetching repository stats: {e}")

    @bot.command()
    async def trending_repos(ctx):
        """Show trending repositories on GitHub."""

        # Define a time range (e.g., last 30 days)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)

        # Format the dates in the format GitHub API expects (YYYY-MM-DD)
        start_date_str = start_date.strftime("%Y-%m-%d")

        # GitHub Search API endpoint
        url = f"https://api.github.com/search/repositories?q=created:>{start_date_str}+stars:>1000&sort=stars&order=desc"

        response = requests.get(url)

        if response.status_code != 200:
            await ctx.send("Error fetching trending repositories.")
            return

        trending_data = response.json()

        # If no repositories found
        if "items" not in trending_data or len(trending_data["items"]) == 0:
            await ctx.send("No trending repositories found.")
            return

        trending_message = "**Trending Repositories**\n\n"

        # Loop through the repositories and get the top 10
        for repo in trending_data["items"][:10]:  # Limit to top 10
            trending_message += f"**{repo['name']}**\n"
            trending_message += f"- 🌟 Stars: {repo['stargazers_count']}\n"
            trending_message += f"- 🍴 Forks: {repo['forks_count']}\n"
            trending_message += f"- 👤 Author: {repo['owner']['login']}\n"
            trending_message += f"- 🔗 [Repository Link]({repo['html_url']})\n\n"

        await ctx.send(trending_message)
