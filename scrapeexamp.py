from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider

from scrapy.spiders import Rule


class WikispyderSpider(CrawlSpider):
    name = "wikiSpyder"

    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Wikipedia:Unusual_articles']

    rules = (
        Rule(LinkExtractor(canonicalize=True, unique=True), follow=True, callback="parse_link"),
    )

    def parse_link(self, response):
        print(response.xpath("//title/text()").extract_first())