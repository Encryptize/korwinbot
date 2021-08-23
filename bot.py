import logging, argparse
from uuid import uuid4

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent

import korwin

# get bot token
parser = argparse.ArgumentParser(description="Bot auth")
parser.add_argument('bot_token', type=str, help='Telegram bot token')
args = parser.parse_args()

# setup bot
bot = Bot(token=args.bot_token)
dp = Dispatcher(bot)

# enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

@dp.inline_handler()
async def inline_handler(update: InlineQuery):
    logger.info(f"User {get_sender_name(update.from_user)} issued inline")
    korwin_response = korwin.korwin_random()

    item = InlineQueryResultArticle(
        id=str(uuid4()),
        title=korwin_response,
        input_message_content=InputTextMessageContent(korwin_response)
    )

    await bot.answer_inline_query(update.id, results=[item], cache_time=1)

@dp.message_handler(commands=['korwin', 'start'])
async def command_handler(update: types.Message):
    logger.info(f"User {get_sender_name(update.from_user)} issued command {update.text}")
    await update.answer(korwin.korwin_random())

def get_sender_name(sender):
    if sender.username:
        return f"@{sender.username} (id: {sender.id})"
    elif sender.first_name and sender.last_name:
        return f"{sender.first_name} {sender.last_name} (id: {sender.id})"
    elif sender.first_name:
        return f"{sender.first_name} (id: {sender.id})"
    else:
        return f"id: {sender.id}"

if __name__ == '__main__':
    executor.start_polling(dp)