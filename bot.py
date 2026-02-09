import os
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from aiohttp import web

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get environment variables
BOT_TOKEN = os.environ.get('BOT_TOKEN')
YOUR_TELEGRAM_ID = os.environ.get('YOUR_TELEGRAM_ID')
KEYWORD = os.environ.get('KEYWORD', '').lower()  # Convert to lowercase for case-insensitive matching
PORT = int(os.environ.get('PORT', 8080))

# Validate environment variables
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is required!")
if not YOUR_TELEGRAM_ID:
    raise ValueError("YOUR_TELEGRAM_ID environment variable is required!")
if not KEYWORD:
    raise ValueError("KEYWORD environment variable is required!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming messages and forward if keyword is found."""
    
    # Get the message
    message = update.message
    
    if not message or not message.text:
        return
    
    # Check if message contains the keyword (case-insensitive)
    if KEYWORD in message.text.lower():
        logger.info(f"Keyword '{KEYWORD}' found in message from user {message.from_user.id}")
        
        # Prepare the forwarded message
        user_info = f"👤 From: {message.from_user.first_name}"
        if message.from_user.username:
            user_info += f" (@{message.from_user.username})"
        user_info += f"\n🆔 ID: {message.from_user.id}"
        
        forwarded_text = (
            f"🔔 Keyword Alert: '{KEYWORD}'\n"
            f"{user_info}\n"
            f"📝 Message:\n{message.text}"
        )
        
        try:
            # Send the message to you
            await context.bot.send_message(
                chat_id=YOUR_TELEGRAM_ID,
                text=forwarded_text
            )
            logger.info(f"Message forwarded successfully to {YOUR_TELEGRAM_ID}")
        except Exception as e:
            logger.error(f"Failed to forward message: {e}")

async def health_check(request):
    """Simple health check endpoint for cron job to ping."""
    return web.Response(text="Bot is alive!")

async def main() -> None:
    """Start the bot."""
    
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add message handler (for all text messages)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Create a simple web server for health check
    app = web.Application()
    app.router.add_get('/', health_check)
    app.router.add_get('/health', health_check)
    
    # Start the web server in the background
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()
    
    logger.info(f"Health check server started on port {PORT}")
    logger.info(f"Bot is running and monitoring for keyword: '{KEYWORD}'")
    logger.info(f"Messages will be forwarded to Telegram ID: {YOUR_TELEGRAM_ID}")
    
    # Start the bot with polling
    await application.initialize()
    await application.start()
    await application.updater.start_polling(drop_pending_updates=True)
    
    # Keep the bot running
    import asyncio
    try:
        await asyncio.Event().wait()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Stopping bot...")
        await application.stop()
        await application.shutdown()
        await runner.cleanup()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
