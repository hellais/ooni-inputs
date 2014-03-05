import codecs
import chardet
import requests
from lxml import etree, html

for i in range(0, 954):
    print "Looking up %s" % i
    res = requests.get('https://en.greatfire.org/search/urls?page=%s' % i)
    encoding = chardet.detect(res.content)['encoding']
    parser = etree.HTMLParser(recover=True, encoding=encoding)
    parsed = etree.fromstring(res.content, parser)
    urls = parsed.xpath('//td[@class="first"]/a/@href')
    with codecs.open('url-list.txt', 'a+', 'utf-8') as f:
        for url in urls:
            data = url[1:]
            if data.startswith('https/'):
                data = data[6:]
                data = 'https://' + data
            f.write(data + '\n')
