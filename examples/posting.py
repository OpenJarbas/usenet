from usenet.server_entry import UsenetServer

USENET_URL = "...."
GROUP = "misc.test"

with UsenetServer(USENET_URL) as server:
    subject = "How does this work"
    text = "this is a test"
    response = server.post(text, subject, GROUP)
    print(response)
