import nntplib
import socket
from datetime import date, timedelta
from usenet.article_entry import Article


class UsenetServer:
    def __init__(self, url, user=None, pswd=None, timeout=3):
        self.url = url
        self.timeout = timeout
        self.user = user
        self.password = pswd
        self._can_post = None
        self._connection = None
        self._capabilities = {}
        self._dead = False
        self._welcome_message = None

    @property
    def can_post(self):
        if not self.capabilities:
            return self._can_post
        return 'POST' in self.capabilities

    @property
    def alive(self):
        return not self._dead

    @property
    def connection(self):
        # lazy connect
        if not self._connection and self.alive:
            self.connect()
        return self._connection

    def connect(self):
        try:
            if self.user and self.password:
                self._connection = nntplib.NNTP(self.url,
                                                user=self.user,
                                                password=self.password,
                                                timeout=self.timeout)
            else:
                self._connection = nntplib.NNTP(self.url, timeout=self.timeout)
        except:
            self._dead = True

    def ping(self):
        try:
            self.connection.getwelcome()
            return True
        except:
            return False

    @property
    def welcome_message(self):
        if not self.connection:
            return "CONNECTION FAILED"
        if not self._welcome_message:
            self._welcome_message = self.connection.getwelcome()
            # parse welcome message for missing info
            if self._can_post is None:
                if "(no posting)" in self._welcome_message:
                    self._can_post = False
                elif "(posting ok)" in self._welcome_message:
                    self._can_post = True
        return self._welcome_message

    def get_new_news(self, GROUP, since=None):
        if isinstance(since, timedelta):
            since = date.today() - since
        since = since or date.today() - timedelta(days=5)
        try:
            response, articles = self.connection.newnews(GROUP, since)
            return [Article(article_id, connection=self.connection)
                    for article_id in articles]
        except (nntplib.NNTPPermanentError, nntplib.NNTPTemporaryError,
                socket.timeout):
            # NEWNEWS command disabled by administrator
            return []

    def get_article(self, article_id):
        try:
            response, article = self.connection.article(article_id)
        except (nntplib.NNTPPermanentError, nntplib.NNTPTemporaryError,
                socket.timeout):
            return None  # no such message (maybe it was deleted?)
        return Article(article.message_id, article.lines)

    def get_groups(self):
        response, groups = self.connection.list()
        return response, groups

    def get_new_groups(self, since=None):
        since = since or date.today() - timedelta(days=5)
        return self.connection.newgroups(since)

    @property
    def capabilities(self):
        if self.connection and not self._capabilities:
            self._capabilities = self.connection.getcapabilities()
        return self._capabilities

    def post(self, text, subject, group, from_address=None, headers=None):
        #response, count, first, last, name = self.connection.group(group)
        headers = headers or {}
        headers["Subject"] = subject
        headers["Newsgroups"] = group
        if "From" not in headers or from_address:
            default_sender = "Anonymous User <anonymous@example.com>"
            headers["From"] = from_address or default_sender
        body = ""
        for k, val in headers.items():
            body += k + ": " + val + "\r\n"
        body += "\r\n" + text
        return self.connection.post(body.encode("utf-8"))

    def quit(self):
        return self.connection.quit()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.quit()
