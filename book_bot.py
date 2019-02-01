import requests
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.dispatcher import run_async
import rfc6266_parser as rfc6266

token = '552105005:AAHdiHL9xU3gG4GTkDP44gKkjGy-OIaxI20'

updater = Updater(token=token)
dispatcher = updater.dispatcher


@run_async
def start_cmd(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Я помогу тебе получить ту книгу, которую ты ищешь. Просто напиши ее название, и я посмотрю, что у меня есть для тебя :)')


@run_async
def book_query(bot, update):
    r = requests.get('https://flbapi.herokuapp.com/', params={'query': update.message.text})
    if r.content:
        result = json.loads(r.content)
        for book in result:
            r_book = requests.get(book['link'])
            filename = rfc6266.parse_requests_response(r_book).filename_unsafe

            if not filename:
                continue

            book_file = open(filename, 'wb')
            book_file.write(r_book.content)
            book_file.close()

            bot.send_message(chat_id=update.message.chat_id, text=('%s[%s]' % (book['name'], book['author'])))
            bot.send_document(chat_id=update.message.chat_id, document=open(filename, 'rb'))
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Увы, я ничего не нашел')


start_command_handler = CommandHandler('start', start_cmd)
text_message_handler = MessageHandler(Filters.text, book_query)


dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)

updater.start_polling(clean=True)
updater.idle()