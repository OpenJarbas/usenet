from usenet import UsenetServer
from datetime import timedelta

USENET_URL = "news2.neva.ru"

with UsenetServer(USENET_URL) as server:
    response, groups = server.get_groups()
    for g in groups:
        print(g.group)
    for article in server.get_new_news('comp.lang.python',
                                       since=timedelta(days=500)):
        print(article.subject, article.date)
        #pprint(article.headers)
        print(article.text)
