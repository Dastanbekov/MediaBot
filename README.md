# MediaDownloaderBot

A Telegram bot for downloading YouTube videos, built with Python and aiogram.

## Features

- Download YouTube videos as MP3 or MP4
- Rate limiting to prevent spam (5 messages/min, 10 clicks/min)
- Admin broadcast messaging system
- User activity tracking and statistics
- Comprehensive error logging

## Requirements

- Python 3.8+
- Telegram Bot Token
- Admin Telegram ID

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/MediaBot.git
cd MediaBot
```

2. Set up virtual environment
```bash
python -m venv env
# Windows
env\Scripts\activate
# Linux/Mac
source env/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create `.env` file with your credentials:
```env
TOKEN=your_telegram_bot_token
ADMIN_ID=your_telegram_id
```

5. Run the bot
```bash
python bot.py
```

## Commands

### User Commands
- `/start` - Start the bot
- `/help` - Show help message
- `/menu` - Open main menu

### Admin Commands
- `/admin` - Access admin panel and statistics
- `/broadcast` - Send message to all users

## Tech Stack

- aiogram 3.16.0 (Telegram Bot Framework)
- yt-dlp (YouTube Download Library)
- SQLite with aiosqlite (Database)
- Python-dotenv (Environment Management)