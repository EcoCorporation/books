# EbookGuy Bot

A powerful, private Telegram Bot designed for managing ebooks, audiobooks, and digital content with premium monetization via Telegram Stars.

## 🚀 Key Features

### Core Features
*   **Private Bot**: Personal 1-on-1 bot experience (no group functionality)
*   **Format Selection**: Users can choose between Ebooks or Audiobooks before searching
*   **Smart Search**: Intelligent file filtering with pagination support
*   **Auto-Delete**: Automatically deletes files after 10 minutes to comply with copyright regulations
*   **Force Subscribe**: Forces users to join specific channels before accessing the bot

### Premium System (Telegram Stars ⭐)
*   **Download Limits**: Free users get 3 downloads per day
*   **Premium Subscriptions**: 6 flexible tiers (1, 7, 15, 30, 60, 90 days)
*   **Telegram Stars Payment**: Native in-app payment - no external gateways needed
*   **Unlimited Downloads**: Premium users enjoy unlimited access
*   **Auto-Renewal Reminders**: Users notified before expiry

### White-Label & Customization
*   **White-Label Ready**: Complete control over branding
*   **Centralized Config**: All text in `Script.py`, settings in `info.py`
*   **Affiliate Integration**: Configure promotional buttons in start message

### Security & Deployment
*   **Secure Deployment**: Docker container runs as non-root user
*   **Backup Channel Support**: "Request Group Link" ensures content access
*   **Smart Indexing**: Efficiently indexes files with checkpoint/resume support
*   **Koyeb/Docker Ready**: Optimized for cloud deployment

## 🛠 Configuration

All configurations are managed in two main files:

1.  **`info.py`**: Contains API keys, database URLs, channel IDs, premium pricing, and affiliate link configurations.
2.  **`Script.py`**: Contains all the text messages used by the bot. Edit this file to change the bot's language or tone.

### Premium Pricing (info.py)
```python
FREE_DAILY_LIMIT = 3  # Free downloads per day
PREMIUM_PRICES = {
    1: 11,    # 1 Day - 11 Stars
    7: 60,    # 7 Days - 60 Stars
    15: 110,  # 15 Days - 110 Stars
    30: 185,  # 30 Days - 185 Stars
    60: 340,  # 60 Days - 340 Stars
    90: 480,  # 90 Days - 480 Stars
}
```

### Affiliate Buttons
You can configure up to 4 affiliate/promotional buttons in `info.py`:
*   `BTN_LABEL_1` / `CHNL_LNK` (Main Channel)
*   `BTN_LABEL_2` / `BTN_URL_2`
*   `BTN_LABEL_3` / `BTN_URL_3`
*   `BTN_LABEL_4` / `BTN_URL_4`

## 🐳 Deployment (Docker)

This bot is optimized for Docker.

1.  **Build the image**:
    ```bash
    docker build -t ebookguy-bot .
    ```

2.  **Run the container**:
    ```bash
    docker run -d -p 8080:8080 --env-file .env ebookguy-bot
    ```

## 🤖 Commands

### General
*   `/start` - Start the bot and choose format (Ebook/Audiobook)
*   `/stats` - Check database statistics
*   `/id` - Get Telegram ID
*   `/info` - Get user info

### Premium & Monetization
*   `/premium` - View premium subscription options with Star pricing
*   `/mystatus` - Check your premium status and remaining downloads

### Premium Admin Commands
*   `/addpremium <user_id> <days>` - Gift premium to a user
*   `/removepremium <user_id>` - Remove premium from a user
*   `/premiumusers` - List all premium subscribers
*   `/stars` - Check bot's Star balance and recent transactions
*   `/starhistory [limit]` - View detailed Star transaction history

### Admin
*   `/logs` - Get recent error logs
*   `/broadcast` - Broadcast message to users
*   `/grp_broadcast` - Broadcast message to groups
*   `/users` - List users
*   `/chats` - List chats
*   `/ban` / `/unban` - Manage user access

### Indexing & Filtering
*   `/index` - Index files from a channel (with checkpoint/resume support)
*   `/delete` - Delete a specific file from DB
*   `/deleteall` - Delete all indexed files
*   `/deletebyquery` - Delete files matching a search query
*   `/filter` - Add a manual filter
*   `/filters` - View all filters
*   `/del` - Delete a filter
*   `/delall` - Delete all filters
*   `/find_duplicates` - Find duplicate files in database

### Extras
*   `/batch` - Create a batch link for multiple files
*   `/link` - Create a link for a single file
*   `/stream` - Generate stream/download links

## 💎 Premium Pricing

| Duration | Price (Stars ⭐) |
|----------|------------------|
| 1 Day    | 11 ⭐            |
| 7 Days   | 60 ⭐            |
| 15 Days  | 110 ⭐           |
| 30 Days  | 185 ⭐           |
| 60 Days  | 340 ⭐           |
| 90 Days  | 480 ⭐           |

## 💎 Premium Benefits

| Feature | Free Users | Premium Users |
|---------|------------|---------------|
| Daily Downloads | 3 per day | Unlimited ∞ |
| Download Speed | Standard | Priority |
| File Access | All files | All files |
| Support | Standard | Priority |

## 📝 License

This project is licensed under the MIT License.
