from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from services.quiz_service import QuizService
from services.s3_service import s3_manager
import logging

logger = logging.getLogger(__name__)


async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    message = update.callback_query.message if update.callback_query else update.message

    async with context.bot_data['db_session'] as session:
        quiz_service = QuizService(session)
        quiz = await quiz_service.generate_quiz()

        context.user_data['current_quiz'] = {
            'character': quiz['character'],
            'correct': quiz['correct_answer']
        }

        # image_url = await s3_manager.get_image_url('hanzi/好.png')
        image_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/Hanzi.svg/1280px-Hanzi.svg.png'
        print("URL", image_url)

        keyboard = [
            [InlineKeyboardButton(option, callback_data=f'answer_{option}')]
            for option in quiz['options']
        ]

        await message.reply_photo(
            photo=image_url,
            caption=f"Что означает этот иероглиф?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    answer = query.data.replace('answer_', '')
    current_quiz = context.user_data.get('current_quiz')
    print('Recieved')

    if not current_quiz:
        await query.edit_message_caption("Quiz session expired. Start a new one with /quiz")
        return

    if answer == current_quiz['correct']:
        await query.edit_message_caption(
            "✅ Верно!\n\n"
            f"{current_quiz['character']} значит: {current_quiz['correct']}n"
            )
        await start_quiz(update, context)
    else:
        await query.edit_message_caption(
            f"❌ Неверно. Ты выбрал: {answer}\n"
            f"Правильный ответ: {current_quiz['correct']}\n\n"
            "Попробуй ещё раз:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Следующий иероглиф", callback_data="next_hanzi")]
            ])
        )

def setup_quiz_handlers(application):
    application.add_handler(CommandHandler("quiz", start_quiz))
    application.add_handler(CallbackQueryHandler(handle_answer, pattern="^answer_"))
    application.add_handler(CallbackQueryHandler(start_quiz, pattern="^next_hanzi"))