from discord import Message

def setup(client):
    @client.event
    async def on_message(message: Message):
        if message.author == client.user:
            return

        print(f"Bot User: {client.user}")
        print(f"Message from {message.author}: {message.content}")

        # Process user message
        user_message = message.content
        await send_message(message, user_message)

# Utility function to send messages
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print("Empty message received.")
        return

    response = f"Hello! You said: {user_message}"
    await message.channel.send(response)
