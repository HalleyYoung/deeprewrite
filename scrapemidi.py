try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule
import scrapy
from scrapy.linkextractors import LinkExtractor

from scrapy.utils.project import get_project_settings
settings = get_project_settings()

settings["DEPTH_LIMIT"] = 6
settings["SCHEDULER_ORDER"] = 'BFO'

def getDomain(url):
   splits = url.split("/")
   print(splits)
   return splits[2] + "/"#"//".join([splits[0], splits[2]]) + "/"

class MidiFind(CrawlSpider):
    def __init__(self):
        super(CrawlSpider, self).__init__()
        self.name = "midifind"
        self.start_urls = ["https://freemidi.org/"]#, "https://www.vgmusic.com/music/console/", "http://midkar.com/", "http://hindimidipalace.tripod.com/index.html", "https://www.cse.iitk.ac.in/users/tvp/music/", "http://www.iskandar.com/joseph/arabicmusiclist.html", "http://arabicmidipalace.tripod.com/index.html"]
        self.allowed_domains = list(map(getDomain, self.start_urls))#["http://www.legco.gov.hk/general/chinese/counmtg/yr04-08/mtg_0708.htm#hansard"]
        #self.rules = [Rule(LinkExtractor(), callback='parse', follow=True)]
    #rules = [Rule(LinkExtractor(), callback='parse', follow=True)]
    name = "midifind"
    start_urls = ["https://freemidi.org/"]#["https://www.vgmusic.com/music/console/", "http://midkar.com/", "http://hindimidipalace.tripod.com/index.html", "https://www.cse.iitk.ac.in/users/tvp/music/", "http://www.iskandar.com/joseph/arabicmusiclist.html", "http://arabicmidipalace.tripod.com/index.html", "https://freemidi.org/"]
    allowed_domains = list(map(getDomain, start_urls))#["http://www.legco.gov.hk/general/chinese/counmtg/yr04-08/mtg_0708.htm#hansard"]
    print("ALLOWED DOMAINS" + str(allowed_domains))

    def parse(self, response):
        base_url = response.url
        print("base url: " + str(base_url))
        for a in response.xpath('//a[@href]/@href'):
            link = a.extract()
            if link.endswith('.midi') or link.endswith(".mid") or link.endswith(".zip"):
                link = urlparse.urljoin(base_url, link)
                yield Request(link, callback=self.save_mid)
        for href in response.xpath('//a/@href').getall():
            print(response.urljoin(href))
            yield scrapy.Request(response.urljoin(href), self.parse)


    def save_mid(self, response):
        splits = response.url.split('/')
        if splits[0].startswith("http"):
            if len(splits[1]) == 0:
                start_ = splits[2].split(".")[1]
            else:
                start_ = splits[3].split(".")[1]
        else:
            start_ = splits[0].split(".")[1]

        fname = splits[-1]

        path = start_ + "-" + fname
        with open("/Users/halley/Documents/midi/" + path, 'wb') as f:
            f.write(response.body)