import scrapy
from scrapy.linkextractor import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider


class DatabloggerScraperItem(scrapy.Item):
    url_from = scrapy.Field()
    url_to = scrapy.Field()


class DatabloggerSpider(CrawlSpider):
    name = "bucharest"
    item_num = 0

    allowed_domains =  ["data-blogger.com"]

    start_urls = ["https://www.data-blogger.com/"]

    rules = [
        Rule(
            LinkExtractor(
                canonicalize=True,
                unique=True
            ),
            follow=True,
            callback="parse_items"
        )
    ]

    def start_requests(self):
        for url in self.start_urls:

            yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse_items(self, response):
        items = []
        links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)
        for link in links:
            is_allowed = False
            for allowed_domain in self.allowed_domains:
                if allowed_domain in link.url:
                    is_allowed = True
            if is_allowed:
                item = DatabloggerScraperItem()
                item['url_from'] = response.url
                item['url_to'] = link.url
                items.append(item)
        self.item_num += 1
        print(self.item_num)
        return items