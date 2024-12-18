# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# bot.cogs.github.stats.py

from discord.ext import commands
from github import Github

def setup(bot):

    db = bot.db
    users_collection = db['users']

    @bot.command()
    @commands.guild_only()
    async def my_contributions(ctx):
        """Show your contributions across all linked repositories."""
        config = users_collection.find_one({"discord_id": ctx.author.id})

        if not config or "github" not in config:
            await ctx.send("GitHub configuration is not set for this user.")
            return

        github_token = config['github']['token']
        github_username = config['github'].get('username')
        repositories = config['github'].get('repos', [])

        if not repositories:
            await ctx.send("No repositories linked to your GitHub configuration.")
            return

        github = Github(github_token)
        total_commits = 0
        total_issues = 0
        total_prs = 0

        try:
            for repo in repositories:
                repo_name = config['github']['github_username'] + '/' + repo.get('name')
                if not repo_name:
                    continue

                repo_instance = github.get_repo(repo_name)

                # Contributions
                commits = repo_instance.get_commits(author=github_username).totalCount
                issues = repo_instance.get_issues(creator=github_username).totalCount
                prs = repo_instance.get_pulls(state="all", creator=github_username).totalCount

                total_commits += commits
                total_issues += issues
                total_prs += prs

            await ctx.send(
                f"**Your Contributions:**\n"
                f"- 📝 Total Commits: {total_commits}\n"
                f"- 🐛 Total Issues Opened: {total_issues}\n"
                f"- 🔀 Total Pull Requests: {total_prs}\n"
            )

        except Exception as e:
            await ctx.send(f"Error fetching your contributions: {e}")
