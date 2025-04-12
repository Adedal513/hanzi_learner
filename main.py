import logging
import asyncio
from time import sleep
from typing import Optional

from telegram.ext import Application, ApplicationBuilder

from config.settings import settings
from handlers.quiz_handlers import setup_quiz_handlers
from services.db_service import Base, db_manager
from services.s3_service import s3_manager


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger  = logging.getLogger(__name__)

async def _initialize_database():
    """Create database tables if they don't exist"""
    async with db_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

class HanziLearningBot:
    """ 
    Main Hanzi Learner bot class.
    """
    def __init__(self):
        self.application: Optional[Application] = None
        self._shutdown_event = asyncio.Event()
    
    async def initialize(self):
        try:
            self.application = (
                ApplicationBuilder()
                .token(settings.TELEGRAM_TOKEN)
                .post_init(self.post_init)
                .post_shutdown(self.post_shutdown)
                .build()
            )

            await self._initialize_services()

            setup_quiz_handlers(self.application)

            logger.info("Bot initialized succesfuly")
        except Exception as e:
            logger.error(f"Failed to initialize bot: {e}")

    async def _initialize_services(self) -> None:
        """Initialize database and storage services"""
        # Initialize S3 bucket if not exists
        try:
            await _initialize_database()
            await s3_manager.create_bucket_if_not_exists()
        except Exception as e:
            logger.warning(f"Service initialization failed: {e}")
            raise

    async def post_init(self, application: Application) -> None:
        logger.info("Bot is starting...")
        application.bot_data['db_session'] = db_manager.async_session_maker()
        logger.info("DB connection established.")
    
    async def post_shutdown(self, application: Application) -> None:
        logger.info("Bot is shutting down...")
    
    async def run(self):
        if not self.application:
            await self.initialize()

def main():
    """Entry point with proper error handling"""
    bot = HanziLearningBot()
    
    # Create new event loop for Windows compatibility
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        loop.run_until_complete(bot.run())
        bot.application.run_polling()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
    finally:
        if not loop.is_closed():
            loop.close()
        logger.info("Bot process terminated")

if __name__ == "__main__":
    main()
