# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderHobbyworldItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    players = scrapy.Field()
    playtime = scrapy.Field()
    price = scrapy.Field()
    tags = scrapy.Field()
    url = scrapy.Field()
    id_bgg = scrapy.Field()
    BGGscore = scrapy.Field()
    difficulty = scrapy.Field()
    debug_link = scrapy.Field()

