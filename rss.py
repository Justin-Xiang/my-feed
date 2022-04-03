from telegram.ext import Updater, CommandHandler
from setting import TOKEN, chat_id
import feedparser
import sqlite3


def init_db():
    conn = sqlite3.connect('rss.db')
    c = conn.cursor()
    c.execute("CREATE TABLE rss (title text, link text, post text)")


def connect_db():
    global conn
    conn = sqlite3.connect('rss.db')
    print("database connect success!")


def sqlite_add(title, link, post):
    connect_db()
    c = conn.cursor()
    print(c)
    data = ((title, link, post))
    c.execute("INSERT INTO rss('title', 'link', 'post') VALUES(?, ?, ?)", data)
    conn.commit()
    conn.close()


def get_all_rss():
    connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM rss")
    rows = c.fetchall()
    conn.close()
    return rows


def add(update, context):
    rss_title = context.args[0]
    rss_link = context.args[1]

    rss_d = feedparser.parse(rss_link)

    length = len(rss_d["entries"]) if len(rss_d["entries"]) < 10 else 10
    for i in range(length):
        sqlite_add(rss_title, rss_link, rss_d["entries"][i]["link"])


def get(update, context):
    for rss in get_all_rss():
        context.bot.send_message(
            chat_id=chat_id, text="Title: "+rss[0]+"\nLink: "+rss[1]+"\nPost: "+rss[2])


def main():
    init_db()
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('add', add))
    dispatcher.add_handler(CommandHandler('get', get))
    updater.start_polling()


if __name__ == '__main__':
    main()
