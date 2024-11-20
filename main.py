import os
from dotenv import load_dotenv
from discord import Intents, Client

# Load environment variables from .env file
load_dotenv()

# Retrieve the token
TOKEN = os.getenv('DISCORD_TOKEN')

if not TOKEN:
    print("DISCORD_TOKEN not found in .env file.")
    exit()

# Setup intents
intents = Intents.default()
intents.message_content = True
intents.members = True
client = Client(intents=intents)


# Load commands (modules)
from commands import events, message

events.setup(client)
message.setup(client)

# Run the bot
try:
    client.run(TOKEN)
except Exception as e:
    print(f"Error starting the bot: {e}")
