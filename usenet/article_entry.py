import dateparser


class Article:
    def __init__(self, article_id, headers=None, body=None, connection=None):
        self.article_id = article_id
        self._headers = headers or {}
        self._body = body
        self.connection = connection

    def bind(self, connection):
        self.connection = connection

    @property
    def headers(self):
        headers = {}
        decoded = self._decode_headers()
        for idx, line in enumerate(decoded):
            if not line:
                continue
            next_line = decoded[idx+1] if \
                idx + 1 < len(decoded) else None
            if next_line and ": " not in next_line:
                line = line + next_line
            if ": " in line:
                fields = line.split(": ")
                val = ": ".join(fields[1:])
                headers[fields[0]] = val
        return headers

    @property
    def text(self):
        return "\n".join(self._decode_body())

    @property
    def subject(self):
        return self.headers['Subject'].replace("\n", " ")

    @property
    def author(self):
        return self.headers['From']

    @property
    def date(self):
        dt = self.headers.get('Date')
        if dt:
            return dateparser.parse(dt)
        return None

    @property
    def language(self):
        return self.headers.get('Content-Language')

    # internal
    def _decode_body(self):
        if self.connection and not self._body:
            # lazy get
            self._get_body()
        if not self._body:
            return ""
        return self._decode(self._body)

    def _decode_headers(self):
        if self.connection and not self._headers:
            # lazy get
            self._get_headers()
        if not self._headers:
            return ""
        return self._decode(self._headers)

    @staticmethod
    def _decode(lines):
        decoded_lines = []
        for l in lines:
            try:
                decoded_lines.append(l.decode("utf-8"))
            except:
                decoded_lines.append("<failed to decode line, binary data?>")
        return decoded_lines

    def _get(self, connection=None):
        connection = connection or self.connection
        try:
            response, article = connection.article(self.article_id)
            if article:
                self.data = article.lines
        except:
            pass

    def _get_body(self, connection=None):
        connection = connection or self.connection
        response, article = connection.body(self.article_id)
        if article:
            self._body = article.lines

    def _get_headers(self, connection=None):
        connection = connection or self.connection
        response, article = connection.head(self.article_id)
        self._headers = article.lines
