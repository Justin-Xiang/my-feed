import feedparser

d = feedparser.parse('http://www.reddit.com/r/python/.rss')
for post in d.entries:
    print(post.title+"\n"+post.link)
print(type(d))