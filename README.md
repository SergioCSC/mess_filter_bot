# Telegram Keyword Filter Bot

A simple Telegram bot that monitors incoming messages and forwards them to you if they contain a specific keyword.

## Features
- ✅ Monitors all messages sent to the bot
- 🔍 Case-insensitive keyword matching
- 📨 Forwards matching messages to your Telegram
- 🌐 Includes health check endpoint for uptime monitoring
- 🔒 Secure environment variable configuration

## Prerequisites
1. Python 3.9+ (for local testing)
2. A Telegram account
3. A GitHub account
4. A Render.com account (free)

## Setup Instructions

### Step 1: Create Your Telegram Bot
1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow the instructions to name your bot
4. **Save the bot token** - you'll need it later (looks like `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Step 2: Get Your Telegram ID
1. Search for `@userinfobot` on Telegram
2. Start a conversation with it
3. It will send you your Telegram ID (a number like `123456789`)
4. **Save this ID** - you'll need it later

### Step 3: Prepare Your Code
1. Create a new repository on GitHub
2. Upload these files to your repository:
   - `bot.py`
   - `requirements.txt`
3. Your repository is now ready!

### Step 4: Deploy to Render.com

1. **Sign up** at [render.com](https://render.com) (it's free!)

2. **Create a New Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your bot repository

3. **Configure the service:**
   - **Name:** Choose any name (e.g., `telegram-keyword-bot`)
   - **Environment:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`
   - **Plan:** Free

4. **Add Environment Variables:**
   Click "Environment" and add these variables:
   
   | Key | Value |
   |-----|-------|
   | `BOT_TOKEN` | Your bot token from @BotFather |
   | `YOUR_TELEGRAM_ID` | Your Telegram ID from @userinfobot |
   | `KEYWORD` | The keyword to monitor (e.g., `urgent`) |

5. **Deploy!** Click "Create Web Service"

Render will build and deploy your bot. This takes 2-3 minutes.

### Step 5: Set Up Cron Job (Keep Bot Awake)

Render's free tier sleeps after 15 minutes of inactivity. Use a cron job to ping it:

1. **Go to [cron-job.org](https://cron-job.org)**
2. **Sign up** for free
3. **Create a new cron job:**
   - Title: `Keep Telegram Bot Awake`
   - URL: Your Render service URL (e.g., `https://your-bot-name.onrender.com/health`)
   - Schedule: Every 10 minutes
   - Click "Create"

Your bot will now stay awake 24/7!

### Step 6: Test Your Bot

1. Open Telegram and search for your bot by username
2. Start a conversation: `/start`
3. Send a message containing your keyword
4. You should receive a forwarded message in your Telegram!

## How It Works

```
User → Sends message to bot → Bot checks for keyword → If found → Forwards to you
```

The bot:
1. Listens for all text messages
2. Checks if the message contains your keyword (case-insensitive)
3. If yes, sends you a notification with:
   - The keyword that was found
   - Who sent it (name, username, ID)
   - The full message text

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `BOT_TOKEN` | Your Telegram bot token from @BotFather | `123456:ABCdef...` |
| `YOUR_TELEGRAM_ID` | Your personal Telegram user ID | `123456789` |
| `KEYWORD` | Keyword to filter (case-insensitive) | `urgent` |
| `PORT` | Port for health check server (auto-set by Render) | `8080` |

## Local Testing (Optional)

If you want to test locally before deploying:

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file (don't commit this!)
cp .env.example .env
# Edit .env with your actual values

# Run the bot
export $(cat .env | xargs) && python bot.py
```

## Security Notes

- ✅ Never commit your `.env` file or tokens to GitHub
- ✅ Always use environment variables on Render (they're encrypted)
- ✅ Your bot token and Telegram ID are safe on Render
- ✅ The `.env.example` file is safe to commit (it has no real values)

## Troubleshooting

**Bot not responding?**
- Check Render logs for errors
- Verify your BOT_TOKEN is correct
- Make sure your bot is not blocked by Telegram

**Not receiving forwarded messages?**
- Verify YOUR_TELEGRAM_ID is correct
- Check if you've started a conversation with the bot
- Look at Render logs for delivery errors

**Bot going to sleep?**
- Ensure cron-job.org is pinging your URL every 10 minutes
- Check the cron job execution history

## Cost

**100% FREE!**
- Render: Free tier (750 hours/month)
- cron-job.org: Free forever
- Telegram Bot API: Free

## Need Help?

Check the logs on Render:
1. Go to your service dashboard
2. Click "Logs" tab
3. Look for error messages

## License

MIT License - feel free to modify and use!
