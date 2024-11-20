from commands import events, message

def setup_bot(client):
    """
    Loads and sets up all required bot modules.

    This function is responsible for registering all events and commands 
    necessary for the bot to function properly.

    Args:
        client (Client): The Discord bot client instance to bind modules to.
    """
    # Register event handling module
    events.setup(client)

    # Register message handling module
    message.setup(client)

    # Log the successful loading of all modules
    print("All modules have been loaded successfully.")
