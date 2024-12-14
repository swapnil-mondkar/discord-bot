# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# bot.cogs.message.py

from bot.extensions.logger import logger

def setup(bot):

    # Define the `/message` command
    @bot.command()
    async def message(ctx, *, user_message: str = None):
        # Check if the user provided a message
        if not user_message:
            await ctx.send("😕 Please provide a message after `/message`. Example: `/message Hello Bot!`")
            return

        # Log the message to MongoDB
        try:
            logger.log_to_mongo(
                author_name=ctx.author.name,
                author_id=str(ctx.author.id),
                message=user_message,
                channel_name=ctx.channel.name,
            )
            print(f"Message logged: {user_message} from {ctx.author.name}")
        except Exception as e:
            logger.log_error(f"Error storing message log: {e}")
            await ctx.send("⚠️ Something went wrong while logging the message. Please try again later.")

        # Process the user message and send a response
        print(f"Bot User: {bot.user}")
        print(f"Message from {ctx.author}: {user_message}")

        # Provide a friendly acknowledgment of the received message
        await ctx.send(f"✔️ Got your message: **{user_message}**. Stored!")
