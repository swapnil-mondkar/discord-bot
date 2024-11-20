from dotenv import load_dotenv
from discord import Client
from intents_setup import setup_intents
from loader import setup_bot
from bot_runner import run_bot

# Load environment variables and initialize the bot
load_dotenv()

# Create the client with intents
client = Client(intents=setup_intents())

# Setup external modules (events and message)
setup_bot(client)

# Run the bot with the token
run_bot(client)
