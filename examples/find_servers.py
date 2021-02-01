from usenet.scrappers import get_elfqrin, get_balocs_list, get_nyx, \
    get_usenettools_isp, get_sok, get_alibis, get_canue

# this includes a few scrappers, but those lists are essentially static
# you should only run this once and extract the urls
# avoid using the scrappers in production code
# valid use cases are statistics and generating an initial list

for s in get_elfqrin():
    print(s.url)

for s in get_nyx():
    print(s.url)

for s in get_balocs_list():
    print(s.url)

for s in get_canue():
    print(s.url)

for s in get_sok():
    print(s.url)

for s in get_usenettools_isp():
    print(s.url)

for s in get_alibis():
    print(s.url)
