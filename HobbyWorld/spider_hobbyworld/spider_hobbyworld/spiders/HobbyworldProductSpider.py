import scrapy
from spider_hobbyworld.items import SpiderHobbyworldItem
import re
from urllib.parse import urlencode

API_KEY = '7a510881b2363c5a7ee66f2a98ff509b'
def build_url(url):
    payload = {'api_key': API_KEY, 'url': url, 'render' : True}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url

class HobbyworldproductspiderSpider(scrapy.Spider):
    name = 'HobbyworldProductSpider'
    allowed_domains = ['hobbygames.ru', 'boardgamegeek.com', 'api.scraperapi.com', 'api.geekdo.com']
    start_urls = ['http://hobbygames.ru/']

    def start_requests(self):
        default_page = 'https://hobbygames.ru/nastolnie?availability=pickup&page='
        for page in range(1, 40):
            query_url = default_page + str(page)
            yield scrapy.Request(url=query_url, callback=self.parse_search_page)

    def parse_search_page(self, response):
        all_links = response.xpath('//div[@class="product-item  "]//a[contains(@class, "name")]/@href').extract()
        for link in all_links:
            yield scrapy.Request(url=link, callback=self.parse_item_page, meta={'url' : link})

    def parse_item_page(self, response):
        item = SpiderHobbyworldItem()
        name = response.xpath('/html/body/div[1]/div/div[4]/div[4]/div[2]/div[1]/div/h1/text()').get()
        players = response.xpath('/html/body/div[1]/div/div[4]/div[4]/div[2]/div[4]/div/div/div[1]/div/span/text()').get()
        playtime = response.xpath('/html/body/div[1]/div/div[4]/div[4]/div[2]/div[4]/div/div/div[2]/div/span/text()').get()
        price = response.xpath('//div[contains(@class, "price-item")]/text()').get()
        tags = response.xpath('//div[@class="tags"]//a//text()').extract()
        tags = [x.strip() for x in tags]
        tags = ' / '.join(tags)
        price = price.replace('\u00A0', '')
        item['name'] = name.strip()
        item['players'] = players.strip()
        item['playtime'] = playtime.strip()
        item['price'] = price.strip()
        item['tags'] = tags
        item['url'] = response.meta['url']

        link = 'https://api.geekdo.com/xmlapi/search?search=' + name
        yield scrapy.Request(url=link, callback=self.search_bgg, meta={'item': item})
        return item

    def search_bgg(self, response):
        item = response.meta['item']
        item['id_bgg'] = response.xpath('./boardgame/@objectid').get()
        link = 'https://api.geekdo.com/xmlapi/boardgame/' + item['id_bgg'] + '?&stats=1'
        yield scrapy.Request(url=link, callback=self.get_score, meta={'item' : item})

    def get_score(self, response):
        item = response.meta['item']
        item['BGGscore'] = response.xpath('//average/text()').get()
        item['difficulty'] = response.xpath('//averageweight/text()').get()

        return item

