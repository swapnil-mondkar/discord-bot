# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# bot.utils.pagination.py

import discord
from math import ceil

async def send_paginated_message(ctx, items, title, description, page_size=10, timeout=60.0):
    """
    Sends a paginated message with navigation reactions.
    
    Parameters:
        ctx: The command context.
        items (list): The list of items to paginate.
        title (str): The embed title.
        description (str): The embed description.
        page_size (int): Number of items per page.
        timeout (float): Timeout for reaction-based navigation.
    """
    total_pages = ceil(len(items) / page_size)
    current_page = 0

    def get_page_embed(page):
        """Generates the embed for the given page."""
        start_index = page * page_size
        end_index = start_index + page_size
        page_items = items[start_index:end_index]

        embed = discord.Embed(
            title=f"{title} (Page {page + 1}/{total_pages})",
            description=description,
            color=discord.Color.blue()
        )

        for item in page_items:
            embed.add_field(
                name=f"**{item['name']}**",
                value=f"**Example:** `{item.get('example', 'N/A')}`\n**Description:** {item.get('description', 'N/A')}",
                inline=False
            )

        return embed

    # Send the first page
    message = await ctx.send(embed=get_page_embed(current_page))

    # Add reaction buttons for navigation if there are multiple pages
    if total_pages > 1:
        await message.add_reaction("⬅️")
        await message.add_reaction("➡️")
    await message.add_reaction("🔄")

    # Reaction listener
    def check(reaction, user):
        return (
            user == ctx.author
            and reaction.message.id == message.id
            and str(reaction.emoji) in ["⬅️", "➡️", "🔄"]
        )

    while True:
        try:
            reaction, user = await ctx.bot.wait_for("reaction_add", timeout=timeout, check=check)

            if str(reaction.emoji) == "⬅️" and current_page > 0:
                current_page -= 1
                await message.edit(embed=get_page_embed(current_page))
            elif str(reaction.emoji) == "➡️" and current_page < total_pages - 1:
                current_page += 1
                await message.edit(embed=get_page_embed(current_page))
            elif str(reaction.emoji) == "🔄":
                # Change page size dynamically
                first_item_index = current_page * page_size
                page_size = 20 if page_size == 10 else 10
                total_pages = ceil(len(items) / page_size)
                current_page = first_item_index // page_size
                await message.edit(embed=get_page_embed(current_page))

            # Remove the user's reaction
            await message.remove_reaction(reaction.emoji, user)

        except discord.errors.Forbidden:
            pass  # Handle if the bot lacks permissions to remove reactions
        except Exception:
            break
