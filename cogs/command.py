# command.py

import discord
from math import ceil

def setup(bot):

    db = bot.db
    cogs_collection = db["commands"]

    @bot.command()
    async def commands(ctx):
        try:
            # Fetch all cogs from MongoDB
            cogs_list = list(cogs_collection.find())  # Convert Cursor to a list

            if len(cogs_list) == 0:  # Check if the list is empty
                await ctx.send("No commands available right now.")
                return

            # Default page size
            page_size = 10
            total_pages = ceil(len(cogs_list) / page_size)
            current_page = 0

            def get_page_embed(page, size):
                """Generates the embed for the given page and page size."""
                start_index = page * size
                end_index = start_index + size
                page_items = cogs_list[start_index:end_index]

                embed = discord.Embed(
                    title=f"Available Commands (Page {page + 1}/{ceil(len(cogs_list) / size)})",
                    description="Here's a list of all the commands you can use:",
                    color=discord.Color.blue()
                )

                for command in page_items:
                    embed.add_field(
                        name=f"**{command['name']}**",
                        value=f"**Example:** `{command['example']}`\n**Description:** {command['description']}",
                        inline=False
                    )

                return embed

            # Send the first page
            message = await ctx.send(embed=get_page_embed(current_page, page_size))

            # Add reaction buttons for navigation and changing page size
            if total_pages > 1:
                await message.add_reaction("⬅️")
                await message.add_reaction("➡️")
            await message.add_reaction("🔄")  # Change page size

            # Reaction listener
            def check(reaction, user):
                return (
                    user == ctx.author
                    and reaction.message.id == message.id
                    and str(reaction.emoji) in ["⬅️", "➡️", "🔄"]
                )

            while True:
                try:
                    reaction, user = await bot.wait_for("reaction_add", timeout=60.0, check=check)

                    # Handle navigation
                    if str(reaction.emoji) == "⬅️" and current_page > 0:
                        current_page -= 1
                        await message.edit(embed=get_page_embed(current_page, page_size))
                    elif str(reaction.emoji) == "➡️" and current_page < total_pages - 1:
                        current_page += 1
                        await message.edit(embed=get_page_embed(current_page, page_size))
                    elif str(reaction.emoji) == "🔄":
                        # Calculate new current page based on current page and page size
                        first_item_index = current_page * page_size
                        page_size = 20 if page_size == 10 else 10
                        total_pages = ceil(len(cogs_list) / page_size)
                        current_page = first_item_index // page_size

                        await message.edit(embed=get_page_embed(current_page, page_size))

                    # Remove the user's reaction
                    await message.remove_reaction(reaction.emoji, user)

                except discord.errors.Forbidden:
                    # If the bot lacks permission to remove reactions
                    pass
                except Exception:
                    break

        except Exception as e:
            await ctx.send("⚠️ Something went wrong while fetching commands.")
            print(f"Error fetching commands: {e}")
