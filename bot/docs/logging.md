# Logging System

The NULL Lab Bot features a robust logging system to track errors and events.

## Logging Locations
1. **File Logs**:
   - Location: `bot.log`
   - Content: Errors and warnings in a readable format.

2. **MongoDB Logs**:
   - Collection: `logs`
   - Content: Detailed information about bot actions, including:
     - Author name
     - Author ID
     - Command message
     - Channel name
     - Timestamp

## Example Log Entry (MongoDB)
```json
{
  "author": "JohnDoe",
  "author_id": "1234567890",
  "message": "!ping",
  "channel": "#general",
  "timestamp": "2024-12-13T14:30:00Z",
  "message_length": 5
}
