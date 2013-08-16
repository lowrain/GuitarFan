from urlparse import urljoin
from urllib2 import *
import json

from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.utils.response import get_base_url
from scrapy.http import Request

from tabcrawler.items import *


class SoSoSpider(CrawlSpider):
    name = 'soso'
    start_urls = ['http://pu.jitapusoso.com']
    allowed_domains = ['jitapusoso.com']
    rules = (
        Rule(SgmlLinkExtractor(allow='singers/[a]\.htm', tags='a'), follow=True),
        # Rule(SgmlLinkExtractor(allow='search/4_.+\.htm', tags='a'), callback='parse_tab_item'),
        Rule(SgmlLinkExtractor(allow='search/4_734b4c466f773d3d\.htm', tags='a'), callback='parse_tab_item'),
    )

    def parse_artist_item(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response)

        # artist_links = hxs.select('//p')[1].select('a')
        #
        # for index, link in enumerate(artist_links):
        #     print link.select('text()').extract()

        hxs = HtmlXPathSelector(response)

        item = LetterArtistItem()
        # html sour like [<span id="tetete">a]</span>
        item['letter'] = hxs.select('//span[@id="tetete"]/text()').extract()[0].rstrip(']')
        item['artists'] = []

        # select all artist links inside second <p> of the page
        artist_links = hxs.select('//p[2]').select('a')
        for index, link in enumerate(artist_links):
            item['artists'].append(link.select('text()').extract()[0])
        yield item


    def parse_tab_item(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response)

        hxs = HtmlXPathSelector(response)

        artist = hxs.select('//p[1]/strong/span/text()').extract()[0]

        if not filter_artist(artist):
            return

        title_links = hxs.select("//p[2]/a[contains(@href, '.htm')]")
        for index, link in enumerate(title_links):
            tab_type = link.select('following-sibling::text()').extract()[0].strip()
            if tab_type == 'img':
                item = TabItem()
                item['artist'] = artist
                item['title'] = link.select('text()').extract()[0].strip()
                item['format'] = tab_type
                tab_url = urljoin(get_base_url(response), link.select('@href').extract()[0])
                request = Request(tab_url, callback=self.parse_imgs)
                request.meta['item'] = item
                yield request
                # yield item


    def parse_imgs(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response)

        hxs = HtmlXPathSelector(response)
        item = response.meta['item']

        item['image_urls'] = []
        imgs = hxs.select("//img[contains(@src, '../allpu/')]")
        for img in imgs:
            img_url = 'http://pu.jitapusoso.com/%s' % img.select('@src').extract()[0][3:]
            item['image_urls'].append(img_url)

        return item


def filter_artist(artist_name):
    with open('json/soso_artists.json') as json_data:
        letter_artist_list = json.load(json_data)

    for letter_dict in letter_artist_list:
        if artist_name in letter_dict['artists']:
            return True

    return False



#
# import urllib2
# import sys
#
# req = urllib2.Request('xxxx.html')
# res = urllib2.urlopen(req)
# html = res.read()
# res.close()
#
# type = sys.getfilesystemencoding()
# html = html.decode('GB2312').encode(type)
# print html
#
#


