import logging
import asyncio
from time import sleep
from typing import Optional

from telegram.ext import Application, ApplicationBuilder

from config.settings import settings
from handlers import setup_handlers


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger  = logging.getLogger(__name__)


class HanziLearningBot:
    """ 
    Main Hanzi Learner bot class.
    """
    def __init__(self):
        self.applcation: Optional[Application] = None
    
    def initialize(self):
        try:
            self.applcation = (
                ApplicationBuilder()
                .token(settings.TELEGRAM_TOKEN)
                .post_init(self.post_init)
                .post_shutdown(self.post_shutdown)
                .build()
            )

            setup_handlers(self.applcation)

            logger.info("Bot initialized succesfuly")
        except Exception as e:
            logger.error(f"Failed to initialize bot: {e}")

    async def post_init(self, application: Application) -> None:
        logger.info("Bot is starting...")
    
    async def post_shutdown(self, application: Application) -> None:
        logger.info("Bot is shutting down...")
    
    def run(self):
        if not self.applcation:
            self.initialize()

        logger.info("Bot is running. Press Ctrl+C to exit.")
        self.applcation.run_polling()


if __name__ == '__main__':
    bot = HanziLearningBot()

    try:
        bot.run()
    except KeyboardInterrupt:
        logger.info("Bot stopped manually")
    except Exception as e:
        logger.critical(f"Bot running error: {e}", exc_info=True)
