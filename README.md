# Telegram Keyword Bot - Google Cloud Functions

Simple serverless Telegram bot that forwards messages containing a keyword.

## Requirements

- Google account
- Credit card (for GCP verification - won't be charged on free tier)
- 10 minutes of setup time

## What You Get

- **100% serverless** - no servers to manage
- **Instant triggers** - webhook-based, responds immediately
- **Free forever** - 2M requests/month free tier (you'll use ~0.1%)
- **Auto-scaling** - handles any load automatically

---

## Setup Guide

### 1. Create Telegram Bot

```bash
# On Telegram:
# 1. Message @BotFather
# 2. Send: /newbot
# 3. Follow prompts
# 4. Save your bot token

# Get your Telegram ID:
# Message @userinfobot
# Save the ID it gives you
```

### 2. Set Up Google Cloud

#### Install gcloud CLI

**macOS:**
```bash
brew install --cask google-cloud-sdk
```

**Windows:**  
Download from: https://cloud.google.com/sdk/docs/install

**Linux:**
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

#### Configure GCP

```bash
# Login
gcloud auth login

# Create new project
gcloud projects create telegram-bot-$(date +%s) --name="Telegram Bot"

# Set project (use the ID from above, or your existing project)
gcloud config set project telegram-bot-XXXXXX

# Enable required APIs
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# Enable billing (required even for free tier)
# Go to: console.cloud.google.com/billing
# Link your project to billing account
```

### 3. Deploy Bot

```bash
# Navigate to your bot directory
cd /path/to/bot/files

# Deploy (replace with your actual values)
gcloud functions deploy telegram-webhook \
  --gen2 \
  --runtime=python312 \
  --region=us-central1 \
  --trigger-http \
  --allow-unauthenticated \
  --entry-point=telegram_webhook \
  --set-env-vars=BOT_TOKEN=your_bot_token,YOUR_TELEGRAM_ID=your_telegram_id,KEYWORD=urgent
```

**Example:**
```bash
gcloud functions deploy telegram-webhook \
  --gen2 \
  --runtime=python312 \
  --region=us-central1 \
  --trigger-http \
  --allow-unauthenticated \
  --entry-point=telegram_webhook \
  --set-env-vars=BOT_TOKEN=123456:ABCdef,YOUR_TELEGRAM_ID=987654321,KEYWORD=urgent
```

Deployment takes ~2 minutes. You'll see:
```
...
url: https://us-central1-PROJECT.cloudfunctions.net/telegram-webhook
...
```

**Save this URL!**

### 4. Set Webhook

```bash
# Replace YOUR_BOT_TOKEN and YOUR_FUNCTION_URL
curl -X POST https://api.telegram.org/botYOUR_BOT_TOKEN/setWebhook \
  -H "Content-Type: application/json" \
  -d '{"url":"YOUR_FUNCTION_URL"}'
```

**Example:**
```bash
curl -X POST https://api.telegram.org/bot123456:ABCdef/setWebhook \
  -H "Content-Type: application/json" \
  -d '{"url":"https://us-central1-telegram-bot-123.cloudfunctions.net/telegram-webhook"}'
```

You should see:
```json
{"ok":true,"result":true,"description":"Webhook was set"}
```

### 5. Test

1. Open Telegram
2. Find your bot and send `/start`
3. Send a message with your keyword: "This is urgent!"
4. You should receive an alert!

---

## Usage

### View Logs

```bash
gcloud functions logs read telegram-webhook --gen2 --region=us-central1 --limit=50
```

### Update Keyword

```bash
gcloud functions deploy telegram-webhook \
  --gen2 \
  --update-env-vars=KEYWORD=new_keyword
```

### Check Webhook Status

```bash
curl https://api.telegram.org/botYOUR_TOKEN/getWebhookInfo
```

### Delete Function

```bash
gcloud functions delete telegram-webhook --gen2 --region=us-central1
```

---

## Troubleshooting

**Bot not responding?**
```bash
# Check logs
gcloud functions logs read telegram-webhook --gen2 --region=us-central1

# Verify webhook
curl https://api.telegram.org/botYOUR_TOKEN/getWebhookInfo

# Test function
curl https://YOUR_FUNCTION_URL
# Should return: "Bot is running"
```

**Deployment failed?**
```bash
# Ensure APIs are enabled
gcloud services enable cloudfunctions.googleapis.com cloudbuild.googleapis.com

# Ensure billing is linked
gcloud billing projects describe $(gcloud config get project)
```

**Permission denied?**
```bash
# Make function public
gcloud functions add-iam-policy-binding telegram-webhook \
  --gen2 \
  --region=us-central1 \
  --member="allUsers" \
  --role="roles/cloudfunctions.invoker"
```

---

## Cost

**Free Tier (Always Free):**
- 2 million requests/month
- 400,000 GB-seconds compute
- 200,000 GHz-seconds CPU

**Your bot's usage:**
- ~100 messages/day = 3,000 requests/month
- **= $0.00** (0.15% of free tier)

Even with 1,000 messages/day you'll stay free.

**After $300 trial:** Always Free tier continues forever.

---

## Files

```
.
├── main.py           # Bot logic
└── requirements.txt  # Dependencies
```

That's it! Simple and clean.

---

## Environment Variables

Set during deployment with `--set-env-vars`:

- `BOT_TOKEN` - From @BotFather
- `YOUR_TELEGRAM_ID` - From @userinfobot  
- `KEYWORD` - What to monitor (case-insensitive)

---

## Modern Python Features Used

- Type hints
- F-strings
- Walrus operator ready (Python 3.12)
- Exception chaining
- JSON built-in
- Dict unpacking

---

## Security

✅ Environment variables encrypted by GCP  
✅ HTTPS only  
✅ No secrets in code  
✅ Minimal dependencies  
✅ Public webhook (Telegram only knows URL)

---

## Need Help?

**Check logs first:**
```bash
gcloud functions logs read telegram-webhook --gen2 --region=us-central1 --limit=50
```

**Verify webhook:**
```bash
curl https://api.telegram.org/botTOKEN/getWebhookInfo
```

**Test function:**
```bash
curl YOUR_FUNCTION_URL
```

---

## Quick Commands

```bash
# Deploy
gcloud functions deploy telegram-webhook --gen2 --runtime=python312 --region=us-central1 --trigger-http --allow-unauthenticated --entry-point=telegram_webhook --set-env-vars=BOT_TOKEN=x,YOUR_TELEGRAM_ID=y,KEYWORD=z

# Logs
gcloud functions logs read telegram-webhook --gen2 --region=us-central1

# Update keyword
gcloud functions deploy telegram-webhook --gen2 --update-env-vars=KEYWORD=new

# Delete
gcloud functions delete telegram-webhook --gen2 --region=us-central1

# Set webhook
curl -X POST https://api.telegram.org/botTOKEN/setWebhook -d '{"url":"URL"}'

# Check webhook
curl https://api.telegram.org/botTOKEN/getWebhookInfo
```

---

**Done! Your serverless bot is live.** 🚀
