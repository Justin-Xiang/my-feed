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


def sqlite_add(title, link, post):
    connect_db()
    c = conn.cursor()
    data = ((title, link, post))
    c.execute("INSERT INTO rss('title', 'link', 'post') VALUES(?, ?, ?)", data)
    conn.commit()
    conn.close()


def get_all_title():
    connect_db()
    c = conn.cursor()
    c.execute("SELECT DISTINCT title from rss")
    rows = c.fetchall()
    conn.close()
    return [title for item in rows for title in item]


def get_filter_rss(title):
    connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM rss WHERE title = ?", (title,))
    rows = c.fetchall()
    conn.close()
    return rows


def get_all_rss():
    connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM rss")
    rows = c.fetchall()
    conn.close()
    return rows


def delete_title(title):
    connect_db()
    c = conn.cursor()
    c.execute("DELETE FROM rss WHERE title = ?", (title,))
    conn.commit()
    conn.close()
    print("删除成功!")


def add(update, context):
    rss_title = context.args[0]
    rss_link = context.args[1]
    rss_d = feedparser.parse(rss_link)
    length = len(rss_d["entries"]) if len(rss_d["entries"]) < 10 else 10
    for i in range(length):
        sqlite_add(rss_title, rss_link, rss_d["entries"][i]["link"])


def get(update, context):
    for rss in get_filter_rss(context.args[0]):
        context.bot.send_message(
            chat_id=chat_id, text="Title: "+rss[0]+"\nLink: "+rss[1]+"\nPost: "+rss[2])


def all(update, context):
    for rss in get_all_rss():
        context.bot.send_message(
            chat_id=chat_id, text="Title: "+rss[0]+"\nLink: "+rss[1]+"\nPost: "+rss[2])


def show(update, context):
    context.bot.send_message(chat_id=chat_id, text=get_all_title())


def delete(update, context):
    delete_title(context.args[0])


def main():
    # init_db()
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('add', add))
    dispatcher.add_handler(CommandHandler('all', all))
    dispatcher.add_handler(CommandHandler("get", get))
    dispatcher.add_handler(CommandHandler("show", show))
    dispatcher.add_handler(CommandHandler("delete", delete))
    updater.start_polling()


if __name__ == '__main__':
    main()
