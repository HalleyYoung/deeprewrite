import urlparse

from scrapy.http import Request
from scrapy.spider import BaseSpider


class MidiFind(BaseSpider):
    name = "midifind"

    allowed_domains = []
    start_urls = allowed_domains#["http://www.legco.gov.hk/general/chinese/counmtg/yr04-08/mtg_0708.htm#hansard"]

    def parse(self, response):
        base_url = scrapy.utils.respose.get_base_url()
        for a in response.xpath('//a[@href]/@href'):
            link = a.extract()
            if link.endswith('.midi') or link.endswith(".mid"):
                link = urlparse.urljoin(base_url, link)
                yield Request(link, callback=self.save_mid)

    def save_mid(self, response):
        path = response.url.split('/')[-1]
        with open(path, 'wb') as f:
            f.write(response.body)