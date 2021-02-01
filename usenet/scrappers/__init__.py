import requests
from usenet.server_entry import UsenetServer


def get_elfqrin(validate=True):
    url = "https://www.elfqrin.com/hacklab/pages/nntpserv.php"
    html = requests.get(url).text.split("c[i]=\"")
    for c in html[1:]:
        server = c.split('"; i++;')[0]
        server = UsenetServer(server)
        if validate:
            server.ping()
            if server.alive:
                yield server
        else:
            yield server


def get_balocs_list(validate=True):
    url = "http://usenet__servers.tripod.com/doc/docpublic.htm"
    html = requests.get(url).text
    trs = html.split("<tr>")[2:]
    for t in trs:
        server, can_post = t.split("</td>")[:-1]
        server = server.split(">")[-1].strip()
        can_post = can_post.split(">")[-1].strip()
        if not server:
            continue
        server = UsenetServer(server)
        server._can_post = can_post
        if validate:
            server.ping()
            if server.alive:
                yield server
        else:
            yield server


def get_nyx(validate=True):
    url = "http://www.nyx.net/~bkraft/"
    html = requests.get(url).text
    trs = html.split("<TR><TD><A HREF=\"")[1:-1]
    for t in trs:
        if not t.startswith("http"):
            continue
        t = t.split('news://')[-1]
        server = t.split('">')[0].rstrip("/").replace("http://", "")
        server = UsenetServer(server)
        if validate:
            server.ping()
            if server.alive:
                yield server
        else:
            yield server


def get_usenettools_isp(validate=True):
    url = "http://www.usenettools.net/ISP.htm"
    html = requests.get(url).text
    # this is ugly, but it works... dont want to drag bs4 requirement for
    # this module that will almost never be used
    for t in html.split('<p class="style4"'):
        t = t.split("</p>")[0].split('">')[-1].replace("<br>", "").replace(
            ">", "").strip()
        if "." not in t:
            continue
        t2s = t.split(" ")
        for t2 in t2s:
            if not t2.strip() or t2.endswith(".") or "." not in t2:
                continue
            server = UsenetServer(t2.strip())
            if validate:
                server.ping()
                if server.alive:
                    yield server
            else:
                yield server


def get_sok(validate=True):
    url = "https://sok.tripod.com/news.html"
    html = requests.get(url).text
    for t in html.split("<tr>")[1:]:
        if "news://" not in t:
            continue
        t = t.split("news://")[-1].split(">")[0].replace('"', "").rstrip("/")
        server = UsenetServer(t)
        if validate:
            server.ping()
            if server.alive:
                yield server
        else:
            yield server


def get_alibis(validate=True):
    url = "https://www.alibis.com/news/help/openlist2.html"
    html = requests.get(url).text
    for t in html.split("<tr>")[1:]:
        if "news://" not in t:
            continue
        t = t.split("news://")[-1].split(">")[0].replace('"', "").rstrip("/")
        server = UsenetServer(t)
        if validate:
            server.ping()
            if server.alive:
                yield server
        else:
            yield server


def get_canue(validate=True):
    for i in range(1, 14):
        url = "http://www.canue.com/nntp/freenewsserver{:02d}.htm".format(i)
        html = requests.get(url).text
        for t in html.split("<li>")[1:]:
            if "news://" not in t:
                continue
            t = t.split("news://")[-1].split(">")[0]\
                .replace('"', "").rstrip("/").replace("http://", "")
            server = UsenetServer(t)
            if validate:
                server.ping()
                if server.alive:
                    yield server
            else:
                yield server
