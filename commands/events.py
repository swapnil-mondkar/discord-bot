from discord import Member, Embed

def setup(client):
    """
    Set up the event handlers for the client.
    """
    # Event for when the bot is ready
    @client.event
    async def on_ready():
        """
        Called when the bot successfully connects to Discord.
        """
        print(f"Logged in as {client.user}!")

    # Event for when a new member joins the server
    @client.event
    async def on_member_join(member: Member):
        """
        Called when a new member joins the server.
        Sends a welcome message in the specified channel.
        """
        specific_channel_id = 1296528681732407408  # Replace with your actual channel ID
        channel = member.guild.get_channel(specific_channel_id)

        if channel:
            embed = Embed(
                title="Welcome to the Server!",
                description=f"We're excited to have you, {member.mention}! 🎉",
                color=0x00ff00  # Green color
            )
            embed.set_thumbnail(url=member.avatar.url)
            embed.add_field(name="Username", value=f"{member.name}#{member.discriminator}", inline=True)
            embed.add_field(name="Member Count", value=f"{member.guild.member_count}", inline=True)
            embed.set_footer(text="Enjoy your stay!")

            await channel.send(embed=embed)
        else:
            print(f"Channel with ID {specific_channel_id} not found. Please check the channel ID.")

    # Event for when a member leaves the server
    @client.event
    async def on_member_remove(member: Member):
        """
        Called when a member leaves the server.
        Sends a goodbye message in the specified channel.
        """
        specific_channel_id = 1296528681732407408  # Replace with your actual channel ID
        channel = member.guild.get_channel(specific_channel_id)

        if channel:
            # Create an embed for the goodbye message
            embed = Embed(
                title="We're sad to see you go...",
                description=f"Goodbye, {member.mention}. We hope to see you again soon! 😢",
                color=0xff0000  # Red color to indicate goodbye
            )
            embed.set_thumbnail(url=member.avatar.url)
            embed.add_field(name="Username", value=f"{member.name}#{member.discriminator}", inline=True)
            embed.add_field(name="Member Count", value=f"{member.guild.member_count}", inline=True)
            embed.set_footer(text="Take care!")

            await channel.send(embed=embed)
        else:
            print(f"Channel with ID {specific_channel_id} not found. Please check the channel ID.")
