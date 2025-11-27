# Advanced Filter Bot

A powerful, fully customizable, and secure Telegram Filter Bot designed for managing files, channels, and groups with ease.

## 🚀 Key Features

*   **White-Label Ready**: Complete control over branding. All text, messages, and buttons are centralized in `Script.py` and `info.py` for easy customization.
*   **Secure Deployment**: Docker container runs as a non-root user for enhanced security.
*   **Affiliate Integration**: Easily configure affiliate/promotional buttons in the start message via `info.py`.
*   **Auto-Delete**: Automatically deletes sensitive files and messages after a set time to comply with copyright regulations.
*   **Backup Channel Support**: "Request Group Link" feature ensures users always have a way to access your content.
*   **Smart Indexing**: Efficiently indexes files from your channels.
*   **Auto-Filter**: Automatically fetches files based on user queries.
*   **Force Subscribe**: Forces users to join specific channels before accessing the bot.
*   **Broadcast**: Send messages to all users or specific groups.

## 🛠 Configuration

All configurations are managed in two main files:

1.  **`info.py`**: Contains API keys, database URLs, channel IDs, and affiliate link configurations.
2.  **`Script.py`**: Contains all the text messages used by the bot. Edit this file to change the bot's language or tone.

### Affiliate Buttons
You can configure up to 3 affiliate/promotional buttons in `info.py`:
*   `BTN_LABEL_1` / `CHNL_LNK` (Main Channel)
*   `BTN_LABEL_2` / `BTN_URL_2`
*   `BTN_LABEL_3` / `BTN_URL_3`
*   `BTN_LABEL_4` / `BTN_URL_4`

## 🐳 Deployment (Docker)

This bot is optimized for Docker.

1.  **Build the image**:
    ```bash
    docker build -t filter-bot .
    ```

2.  **Run the container**:
    ```bash
    docker run -d -p 8080:8080 --env-file .env filter-bot
    ```

## 🤖 Commands

### General
*   `/start` - Start the bot
*   `/stats` - Check database statistics
*   `/id` - Get Telegram ID
*   `/info` - Get user info

### Admin
*   `/logs` - Get recent error logs
*   `/broadcast` - Broadcast message to users
*   `/grp_broadcast` - Broadcast message to groups
*   `/users` - List users
*   `/chats` - List chats
*   `/ban` / `/unban` - Manage user access

### Indexing & Filtering
*   `/index` - Index files from a channel
*   `/delete` - Delete a specific file from DB
*   `/deleteall` - Delete all indexed files
*   `/filter` - Add a manual filter
*   `/filters` - View all filters
*   `/del` - Delete a filter
*   `/delall` - Delete all filters

### Group Management
*   `/connect` - Connect group to PM
*   `/disconnect` - Disconnect group
*   `/settings` - Open settings menu
*   `/fsub` - Add force subscribe channel
*   `/nofsub` - Remove force subscribe

### Extras
*   `/batch` - Create a batch link for multiple files
*   `/link` - Create a link for a single file
*   `/shortlink` - Configure URL shortener
*   `/stream` - Generate stream/download links

## 📝 License

This project is licensed under the MIT License.
