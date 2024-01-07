import os
from aiogram import types
from search import search_in_file, send_results
from utils import PATH, stats

def setup_handlers(dp, executor, bot):
    @dp.message_handler(commands=['start'])
    async def start(message: types.Message):
        keyboard = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Search', callback_data='search') 
        btn2 = types.InlineKeyboardButton('Statistics', callback_data='stats') 
        keyboard.add(btn1, btn2)
        await message.answer('Choose an action:', reply_markup=keyboard)

    @dp.callback_query_handler(lambda c: c.data == 'search')
    async def process_callback_search(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, 'Enter the text to search:')

    @dp.callback_query_handler(lambda c: c.data == 'stats')
    async def process_callback_stats(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, f"Files processed: {stats['files_processed']}, errors: {stats['errors']}")

    @dp.message_handler()
    async def handle_message(message: types.Message):
        text = message.text
        chat_id = message.chat.id
        for filename in os.listdir(PATH):
            try:
                if filename.endswith(('.csv', '.txt', '.json')):
                    future = executor.submit(search_in_file, filename, text)
                    future.add_done_callback(lambda x: send_results(bot, x.result(), chat_id))
            except Exception as e:
                print(f"Error processing file {filename}: {e}")
                stats['errors'] += 1