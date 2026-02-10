# Quick Start Guide - 5 Minutes

## Prerequisites
- [ ] Google account
- [ ] Credit card (for GCP verification)
- [ ] gcloud CLI installed

## Step 1: Create Bot (2 min)
```
1. Telegram → @BotFather → /newbot
2. Save token: 123456:ABCdef...
3. Telegram → @userinfobot
4. Save ID: 123456789
```

## Step 2: Setup GCP (2 min)
```bash
# Login
gcloud auth login

# Create project
gcloud projects create my-telegram-bot-$(date +%s)

# Use it
gcloud config set project my-telegram-bot-XXXXXX

# Enable APIs
gcloud services enable cloudfunctions.googleapis.com cloudbuild.googleapis.com

# Enable billing at: console.cloud.google.com/billing
```

## Step 3: Deploy (1 min)
```bash
# Option A: Use script
./deploy.sh

# Option B: Manual
gcloud functions deploy telegram-webhook \
  --gen2 \
  --runtime=python312 \
  --region=us-central1 \
  --trigger-http \
  --allow-unauthenticated \
  --entry-point=telegram_webhook \
  --set-env-vars=BOT_TOKEN=xxx,YOUR_TELEGRAM_ID=yyy,KEYWORD=urgent
```

## Step 4: Set Webhook (30 sec)
```bash
# Get your function URL from deployment output, then:
curl -X POST https://api.telegram.org/botYOUR_TOKEN/setWebhook \
  -d '{"url":"YOUR_FUNCTION_URL"}'
```

## Step 5: Test!
Send message with keyword to your bot → Get alert!

---

## Troubleshooting

**Not working?**
```bash
# Check logs
gcloud functions logs read telegram-webhook --gen2 --region=us-central1 --limit=20

# Check webhook
curl https://api.telegram.org/botYOUR_TOKEN/getWebhookInfo
```

**Cost?**
Free forever! (2M requests/month, you'll use ~3,000)

---

## Daily Use

No maintenance needed! It just works 24/7.

**To update keyword:**
```bash
gcloud functions deploy telegram-webhook --gen2 --update-env-vars=KEYWORD=new_word
```

**To view activity:**
```bash
gcloud functions logs read telegram-webhook --gen2 --region=us-central1
```

That's it! 🎉
