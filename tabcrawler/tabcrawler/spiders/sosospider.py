from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector

from tabcrawl.items import *

class SoSoSpider(CrawlSpider):
    name = 'soso'
    start_urls = ['http://pu.jitapusoso.com']
    allowed_domains = ['jitapusoso.com']
    rules = (
        Rule(SgmlLinkExtractor(allow='singers/[a]\.htm', tags='a'), follow=True, callback='parse_artist_item'),
        # Rule(SgmlLinkExtractor(allow='search/4_.+\.htm', tags='a'), callback='parse_tab_item'),
        Rule(SgmlLinkExtractor(allow='search/4_734b7a4270722f4c774c50473162625a\.htm', tags='a'), callback='parse_tab_item'),
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

        item = ArtistTabItem()
        item['artist'] = hxs.select('//p[1]').select('strong/span/text()').extract()[0]
        item['tabs'] = []
        title_links = hxs.select('//p[2]').select("a[contains(@href, '.htm')]")
        for index, link in enumerate(title_links):
            tab_type = link.select('following-sibling::text()').extract()[0].strip()
            if tab_type == 'img':
                item['tabs'].append(link.select('text()').extract()[0].strip())

        yield item
