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
    bot.send_message(chat_id=update.message.chat_id, text='365 395 книг и 132 763 автора бесплатно, быстро и удобно. Скачивайте свои любимые книги в формате EPUB. \n\nРугаться и любить сюда - @lipovoowa')

@run_async
def book_query(bot, update):
    r = requests.get('https://flbapi.herokuapp.com/', params={'query': update.message.text, 'chat_id': update.message.chat_id})
    if not r.content:
        r = requests.get('https://flbapi.herokuapp.com/',  params={'query': update.message.text, 'chat_id': update.message.chat_id})
    if r.content:
        result = json.loads(r.content)
        if bool(result):
            bot.send_message(chat_id=update.message.chat_id, text='Хм, посмотрим, что я смог найти:')
            count = 0
            for book in result:
                r_book = requests.get(book['link'])
                if r_book.headers['content-type'] == 'text/html; charset=utf-8':
                    continue

                filename = rfc6266.parse_requests_response(r_book).filename_unsafe
                book_file = open(filename, 'wb')
                book_file.write(r_book.content)
                book_file.close()
                bot.send_document(chat_id=update.message.chat_id, caption=('%s[%s]' % (book['name'], book['author'])), document=open(filename, 'rb'))
                count += 1
                if count >= 6:
                    break
        else:
            bot.send_message(chat_id=update.message.chat_id, text='Увы, я ничего не нашел')

    else:
        bot.send_message(chat_id=update.message.chat_id, text='Увы, я ничего не нашел')


start_command_handler = CommandHandler('start', start_cmd)
text_message_handler = MessageHandler(Filters.text, book_query)


dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)

updater.start_polling(clean=True)
updater.idle()