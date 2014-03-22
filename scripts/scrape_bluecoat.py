import yaml
import json
import codecs
import chardet
import requests
from lxml import etree, html

def add_to_yaml_doc(content, fn='bluecoat-categories.yml'):
    d = {}
    try:
        with open(fn) as f:
            d = yaml.load(f)
    except: pass

    d.update(content)
    with open(fn, 'w+') as f:
        yaml.dump(d, f)

res = requests.get('http://sitereview.bluecoat.com/rest/categoryList')
category_list = json.loads(res.content)
for category in category_list:
    categories = {}
    url = "http://testrating.webfilter.bluecoat.com/%s" % category['name']
    res = requests.get(url)
    encoding = chardet.detect(res.content)['encoding']
    parser = etree.HTMLParser(recover=True, encoding=encoding)
    parsed = etree.fromstring(res.content, parser)
    categories[str(category['name'])] = map(str, parsed.xpath('//a/@href'))
    add_to_yaml_doc(categories) 
