from discord import Member, Embed

def setup(client):
    @client.event
    async def on_ready():
        print(f"Logged in as {client.user}!")

    @client.event
    async def on_member_join(member: Member):
        specific_channel_id = 1296528681732407408  # Replace with your channel ID
        channel = member.guild.get_channel(specific_channel_id)

        if channel:
            embed = Embed(
                title="Welcome to the Server!",
                description=f"We're excited to have you, {member.mention}! 🎉",
                color=0x00ff00
            )
            embed.set_thumbnail(url=member.avatar.url)
            embed.add_field(name="Username", value=f"{member.name}#{member.discriminator}", inline=True)
            embed.add_field(name="Member Count", value=f"{member.guild.member_count}", inline=True)
            embed.set_footer(text="Enjoy your stay!")
            await channel.send(embed=embed)
        else:
            print(f"Channel with ID {specific_channel_id} not found.")

    @client.event
    async def on_member_remove(member: Member):
        specific_channel_id = 1296528681732407408  # Replace with your channel ID
        channel = member.guild.get_channel(specific_channel_id)

        if channel:
            await channel.send(f"Goodbye, {member.mention}. We're sad to see you leave! 😢")
        else:
            print(f"Channel with ID {specific_channel_id} not found.")
