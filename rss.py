from asyncore import dispatcher
import telegram
from telegram.ext import Updater, CallbackContext, CommandHandler
from setting import TOKEN, chat_id
import feedparser

rss_list = []

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher


def add(update, context):
    rss_list.append(context.args[0])


def get(update, context):
    for rss_url in rss_list:
        d = feedparser.parse(rss_url)
        for post in d.entries:
            context.bot.send_message(
                chat_id=chat_id, text=post.title+"\n"+post.link)


dispatcher.add_handler(CommandHandler('add', add))
dispatcher.add_handler(CommandHandler('get', get))

updater.start_polling()
