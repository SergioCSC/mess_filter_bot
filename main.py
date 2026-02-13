"""
Telegram Keyword Filter Bot - Google Cloud Function
Serverless webhook handler that forwards messages containing a keyword.
"""

import gspread
import google.auth

import os
import json
import logging
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
BOT_TOKEN = os.environ.get('BOT_TOKEN')
YOUR_TELEGRAM_ID = os.environ.get('YOUR_TELEGRAM_ID')
KEYWORD = os.environ.get('KEYWORD', '').lower()
GOOGLE_SHEET_ID = os.environ.get('GOOGLE_SHEET_ID')

# Telegram API endpoint
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"


def send_message(chat_id: str, text: str) -> bool:
    """Send a message via Telegram Bot API."""
    try:
        response = requests.post(
            f"{TELEGRAM_API}/sendMessage",
            json={'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'},
            timeout=10
        )
        response.raise_for_status()
        logger.info(f"Message sent to {chat_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to send message: {e}")
        return False


def write_to_sheet(s: str) -> None:
    # 1. Автоматическое получение прав самой функции
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    creds, project = google.auth.default(scopes=scopes)
    
    # 2. Авторизация в gspread
    client = gspread.authorize(creds)
    
    # 3. Открытие таблицы по ID (из URL таблицы)
    sheet_id = GOOGLE_SHEET_ID
    spreadsheet = client.open_by_key(sheet_id)
    worksheet = spreadsheet.get_worksheet(0) # первый лист
    
    # 4. Запись данных
    worksheet.append_row(['Hello', 'from', 'Cloud Function!', '', s])
    
    return


def telegram_webhook(request):
    """
    Cloud Function entry point.
    Handles incoming webhook requests from Telegram.
    """
    
    # Validate configuration
    if not all([BOT_TOKEN, YOUR_TELEGRAM_ID, KEYWORD]):
        logger.error("Missing required environment variables")
        return ('Configuration error', 500)
    
    # Handle GET requests (health check)
    if request.method == 'GET':
        return ('Bot is running', 200)
    
    # Parse webhook payload
    try:
        update = request.get_json(silent=True)
        if not update:
            return ('OK', 200)
        
        logger.info(f"Received update: {json.dumps(update)[:200]}")
    except Exception as e:
        logger.error(f"Failed to parse request: {e}")
        return ('Invalid request', 400)
    
    # Extract message
    message = update.get('message', {})
    text = message.get('text', '')
    
    if not text:
        return ('OK', 200)
    
    # Check for keyword
    if KEYWORD not in text.lower():
        logger.info(f"No keyword match in message")
        return ('OK', 200)
    
    # Keyword found - prepare alert
    user = message.get('from', {})
    user_name = user.get('first_name', 'Unknown')
    user_username = user.get('username')
    user_id = user.get('id', 'Unknown')
    
    alert = (
        f"🔔 <b>Keyword Alert: '{KEYWORD}'</b>\n\n"
        f"👤 From: {user_name}"
        f"{f' (@{user_username})' if user_username else ''}\n"
        f"🆔 ID: {user_id}\n\n"
        f"📝 <b>Message:</b>\n{text}"
    )
    
    write_to_sheet(alert)
    
    # Send alert
    send_message(YOUR_TELEGRAM_ID, alert)
    logger.info(f"Alert sent for keyword '{KEYWORD}'")
    
    return ('OK', 200)
