# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# github.py

from github import Github
from datetime import datetime, timedelta

def setup(bot):

    GITHUB_TOKEN = "token"
    REPO_NAME = "swapnil-mondkar/Discord-Bot" 
    github = Github(GITHUB_TOKEN)

    @bot.command()
    async def daily_contributions(ctx):
        repo = github.get_repo(REPO_NAME)
        commits = repo.get_commits(since=datetime.now() - timedelta(days=1))

        contributions = {}
        for commit in commits:
            author = commit.author.login if commit.author else "Unknown"
            contributions[author] = contributions.get(author, 0) + 1

        if not contributions:
            await ctx.send("No contributions in the last 24 hours.")
            return

        contribution_message = "Daily Contributions:\n"
        for author, count in contributions.items():
            contribution_message += f"- {author}: {count} commits\n"

        await ctx.send(contribution_message)
