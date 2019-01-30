import requests
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

token = '552105005:AAHdiHL9xU3gG4GTkDP44gKkjGy-OIaxI20'

updater = Updater(token=token)
dispatcher = updater.dispatcher


def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Я помогу тебе получить ту книгу, которую ты ищешь. Просто напиши ее название, и я посмотрю, что у меня есть для тебя :)')


def textMessage(bot, update):
    r = requests.get('https://flbapi.herokuapp.com/', params={'query': update.message.text})
    if r.content:
        result = json.loads(r.content)
        for book in result:
            r_book = requests.get(book['link'])
            bot.send_message(chat_id=update.message.chat_id, text=r_book.status_code)

            book_file = open(r'books/%s[%s].epub' % (book['name'], book['author']), 'wb')
            book_file.write(r_book.content)
            book_file.close()

            bot.send_document(chat_id=update.message.chat_id, document=open('books/%s[%s].epub' % (book['name'], book['author']), 'rb'))
            #bot.send_message(chat_id=update.message.chat_id, text=book['name'])


start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)


dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)

updater.start_polling(clean=True)
updater.idle()